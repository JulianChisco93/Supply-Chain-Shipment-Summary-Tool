"""
shipment_summary.py

Descriptive analysis of shipment activities from the supply delivery history dataset.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.gridspec as gridspec
import seaborn as sns

from src.data_loader import load_clean_data


# ---------------------------------------------------------------------
# Data loading and preparation
# ---------------------------------------------------------------------

def load_shipment_dataset() -> pd.DataFrame:
    """
    Load the cleaned shipment dataset.
    Returns:
        pd.DataFrame
    """
    return load_clean_data()


def prepare_shipment_data(df: pd.DataFrame | None = None) -> pd.DataFrame:
    """
    Select and prepare shipment-related columns for analysis.
    Adds derived fields:
        - Delivery Delay Days: difference between delivered and scheduled date.
        - Delivery Year: calendar year of the actual delivery.
    Returns:
        pd.DataFrame: Prepared shipment-level dataset.
    """
    if df is None:
        df = load_shipment_dataset()

    shipment_df = df.copy()

    required_columns = [
        "ID",
        "Country",
        "Fulfill Via",
        "Shipment Mode",
        "Scheduled Delivery Date",
        "Delivered to Client Date",
        "Delivery Recorded Date",
        "Product Group",
        "Line Item Quantity",
        "Line Item Value",
        "Weight (Kilograms)",
        "Freight Cost (USD)",
        "Line Item Insurance (USD)",
    ]

    available_columns = [col for col in required_columns if col in shipment_df.columns]
    shipment_df = shipment_df[available_columns].copy()

    # Convert date columns to datetime
    for col in ("Scheduled Delivery Date", "Delivered to Client Date", "Delivery Recorded Date"):
        if col in shipment_df.columns:
            shipment_df[col] = pd.to_datetime(shipment_df[col], errors="coerce")

    # Numeric coercion for shipment metrics
    numeric_cols = [
        "Line Item Quantity",
        "Line Item Value",
        "Weight (Kilograms)",
        "Freight Cost (USD)",
        "Line Item Insurance (USD)",
    ]
    for col in numeric_cols:
        if col in shipment_df.columns:
            shipment_df[col] = pd.to_numeric(shipment_df[col], errors="coerce")

    # Delivery Delay Days (positive = late, negative = early)
    if "Scheduled Delivery Date" in shipment_df.columns and "Delivered to Client Date" in shipment_df.columns:
        shipment_df["Delivery Delay Days"] = (
            shipment_df["Delivered to Client Date"] - shipment_df["Scheduled Delivery Date"]
        ).dt.days

    # Delivery Year from actual delivery date
    if "Delivered to Client Date" in shipment_df.columns:
        shipment_df["Delivery Year"] = shipment_df["Delivered to Client Date"].dt.year

    return shipment_df


# ---------------------------------------------------------------------
# Summary and insight functions
# ---------------------------------------------------------------------

def get_shipment_overview(df: pd.DataFrame | None = None) -> pd.DataFrame:
    """
    Return a single-row DataFrame of high-level shipment metrics:
        - Total Records
        - Total Line Item Quantity
        - Total Line Item Value (USD)
        - Total Weight (Kilograms)
        - Total Freight Cost (USD)
        - Average Delivery Delay (Days)
        - Earliest Delivery Date
        - Latest Delivery Date
    Returns:
        pd.DataFrame: One-row summary.
    """
    shipment_df = prepare_shipment_data(df)

    overview = pd.DataFrame([{
        "Total Records": len(shipment_df),
        "Total Line Item Quantity": shipment_df["Line Item Quantity"].sum(),
        "Total Line Item Value (USD)": shipment_df["Line Item Value"].sum(),
        "Total Weight (Kilograms)": shipment_df["Weight (Kilograms)"].sum(),
        "Total Freight Cost (USD)": shipment_df["Freight Cost (USD)"].sum(),
        "Average Delivery Delay (Days)": shipment_df["Delivery Delay Days"].mean().round(2)
            if "Delivery Delay Days" in shipment_df.columns else None,
        "Earliest Delivery": shipment_df["Delivered to Client Date"].min()
            if "Delivered to Client Date" in shipment_df.columns else None,
        "Latest Delivery": shipment_df["Delivered to Client Date"].max()
            if "Delivered to Client Date" in shipment_df.columns else None,
    }])

    return overview


def summarize_by_shipment_mode(df: pd.DataFrame | None = None) -> pd.DataFrame:
    """
    Summarize shipment activity grouped by Shipment Mode.
    Returns:
        pd.DataFrame: Per-mode summary sorted by shipment count descending.
    """
    shipment_df = prepare_shipment_data(df)

    agg: dict = {
        "ID": "count",
        "Line Item Quantity": "sum",
        "Line Item Value": "sum",
        "Weight (Kilograms)": "sum",
        "Freight Cost (USD)": "mean",
    }
    if "Delivery Delay Days" in shipment_df.columns:
        agg["Delivery Delay Days"] = "mean"

    summary = (
        shipment_df
        .groupby("Shipment Mode", as_index=False)
        .agg(agg)
        .rename(columns={
            "ID": "Shipment_Records",
            "Line Item Quantity": "Total_Quantity",
            "Line Item Value": "Total_Value",
            "Weight (Kilograms)": "Total_Weight_Kg",
            "Freight Cost (USD)": "Avg_Freight_Cost_USD",
            "Delivery Delay Days": "Avg_Delay_Days",
        })
        .sort_values("Shipment_Records", ascending=False)
        .reset_index(drop=True)
    )

    if "Avg_Delay_Days" in summary.columns:
        summary["Avg_Delay_Days"] = summary["Avg_Delay_Days"].round(2)
    summary["Avg_Freight_Cost_USD"] = summary["Avg_Freight_Cost_USD"].round(2)

    return summary


def summarize_by_fulfill_type(df: pd.DataFrame | None = None) -> pd.DataFrame:
    """
    Compare shipment activity between Direct Drop and From RDC fulfillment types.
    Returns:
        pd.DataFrame: Per-fulfillment-type summary.
    """
    shipment_df = prepare_shipment_data(df)

    agg: dict = {
        "ID": "count",
        "Line Item Quantity": "sum",
        "Line Item Value": "sum",
        "Weight (Kilograms)": "sum",
        "Freight Cost (USD)": "mean",
    }
    if "Delivery Delay Days" in shipment_df.columns:
        agg["Delivery Delay Days"] = "mean"

    summary = (
        shipment_df
        .groupby("Fulfill Via", as_index=False)
        .agg(agg)
        .rename(columns={
            "ID": "Shipment_Records",
            "Line Item Quantity": "Total_Quantity",
            "Line Item Value": "Total_Value",
            "Weight (Kilograms)": "Total_Weight_Kg",
            "Freight Cost (USD)": "Avg_Freight_Cost_USD",
            "Delivery Delay Days": "Avg_Delay_Days",
        })
        .sort_values("Shipment_Records", ascending=False)
        .reset_index(drop=True)
    )

    if "Avg_Delay_Days" in summary.columns:
        summary["Avg_Delay_Days"] = summary["Avg_Delay_Days"].round(2)
    summary["Avg_Freight_Cost_USD"] = summary["Avg_Freight_Cost_USD"].round(2)

    return summary


def summarize_shipments_over_time(df: pd.DataFrame | None = None) -> pd.DataFrame:
    """
    Summarize shipment records, total value, and total quantity by delivery year.
    Returns:
        pd.DataFrame: Year-level summary sorted chronologically.
    """
    shipment_df = prepare_shipment_data(df)

    if "Delivery Year" not in shipment_df.columns:
        raise ValueError("Delivery Year column is missing — check date parsing.")

    summary = (
        shipment_df
        .dropna(subset=["Delivery Year"])
        .groupby("Delivery Year", as_index=False)
        .agg(
            Shipment_Records=("ID", "count"),
            Total_Quantity=("Line Item Quantity", "sum"),
            Total_Value=("Line Item Value", "sum"),
            Total_Freight_Cost=("Freight Cost (USD)", "sum"),
        )
        .sort_values("Delivery Year")
        .reset_index(drop=True)
    )

    summary["Delivery Year"] = summary["Delivery Year"].astype(int)

    return summary


def get_top_countries_by_shipments(
    df: pd.DataFrame | None = None,
    top_n: int = 10
) -> pd.DataFrame:
    """
    Return the top countries by number of shipment records.
    Returns:
        pd.DataFrame: Top countries with shipment counts and total value.
    """
    shipment_df = prepare_shipment_data(df)

    summary = (
        shipment_df
        .groupby("Country", as_index=False)
        .agg(
            Shipment_Records=("ID", "count"),
            Total_Quantity=("Line Item Quantity", "sum"),
            Total_Value=("Line Item Value", "sum"),
        )
        .sort_values("Shipment_Records", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    return summary


# ---------------------------------------------------------------------
# Visualizations
# ---------------------------------------------------------------------

def plot_shipments_by_mode(df: pd.DataFrame | None = None, pre_ax=None) -> None:
    """
    Bar chart of shipment record count by Shipment Mode.
    """
    summary = summarize_by_shipment_mode(df)

    created_internal_figure = False
    if pre_ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))
        created_internal_figure = True
    else:
        ax = pre_ax

    sns.barplot(
        x="Shipment Mode",
        y="Shipment_Records",
        data=summary,
        palette="Blues_d",
        ax=ax,
    )

    ax.set_title("Shipment Records by Mode", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Shipment Mode", fontsize=11)
    ax.set_ylabel("Number of Shipments", fontsize=11)
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)
    sns.despine()

    for bar in ax.patches:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{int(height):,}",
            ha="center", va="bottom", fontsize=9,
        )

    if created_internal_figure:
        plt.tight_layout()
        plt.show()


def plot_value_by_mode(df: pd.DataFrame | None = None, pre_ax=None) -> None:
    """
    Bar chart of total line item value by Shipment Mode.
    """
    summary = summarize_by_shipment_mode(df)

    created_internal_figure = False
    if pre_ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))
        created_internal_figure = True
    else:
        ax = pre_ax

    sns.barplot(
        x="Shipment Mode",
        y="Total_Value",
        data=summary,
        palette="Greens_d",
        ax=ax,
    )

    ax.set_title("Total Shipment Value by Mode", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Shipment Mode", fontsize=11)
    ax.set_ylabel("Total Value (USD)", fontsize=11)
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x/1_000_000:,.0f}M"))
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)
    sns.despine()

    if created_internal_figure:
        plt.tight_layout()
        plt.show()


def plot_shipments_over_time(df: pd.DataFrame | None = None, pre_ax=None) -> None:
    """
    Line chart of shipment records per year.
    """
    time_df = summarize_shipments_over_time(df)

    created_internal_figure = False
    if pre_ax is None:
        fig, ax = plt.subplots(figsize=(12, 5))
        created_internal_figure = True
    else:
        ax = pre_ax

    ax.plot(
        time_df["Delivery Year"],
        time_df["Shipment_Records"],
        marker="o",
        linewidth=2.5,
        color="#4FA3D1",
    )

    ax.set_title("Shipment Records Over Time", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Year", fontsize=11)
    ax.set_ylabel("Number of Shipments", fontsize=11)
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="both", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)
    sns.despine()

    if created_internal_figure:
        plt.tight_layout()
        plt.show()


def plot_top_countries_by_shipments(
    df: pd.DataFrame | None = None,
    top_n: int = 10,
    pre_ax=None,
) -> None:
    """
    Horizontal bar chart of top countries by shipment record count.
    """
    summary = get_top_countries_by_shipments(df, top_n=top_n)

    created_internal_figure = False
    if pre_ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
        created_internal_figure = True
    else:
        ax = pre_ax

    sns.barplot(
        x="Shipment_Records",
        y="Country",
        data=summary,
        palette="Blues_r",
        ax=ax,
    )

    ax.set_title(f"Top {top_n} Countries by Shipments", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Shipment Records", fontsize=11)
    ax.set_ylabel("Country", fontsize=11)
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{int(x):,}"))

    for i, value in enumerate(summary["Shipment_Records"]):
        ax.text(
            value + (summary["Shipment_Records"].max() * 0.01),
            i,
            f"{int(value):,}",
            va="center", fontsize=9,
        )

    ax.grid(axis="x", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)
    sns.despine()

    if created_internal_figure:
        plt.tight_layout()
        plt.show()


def plot_fulfill_type_comparison(df: pd.DataFrame | None = None, pre_ax=None) -> None:
    """
    Bar chart comparing shipment records by fulfillment type.
    """
    summary = summarize_by_fulfill_type(df)

    created_internal_figure = False
    if pre_ax is None:
        fig, ax = plt.subplots(figsize=(7, 5))
        created_internal_figure = True
    else:
        ax = pre_ax

    sns.barplot(
        x="Fulfill Via",
        y="Shipment_Records",
        data=summary,
        palette="Oranges_d",
        ax=ax,
    )

    ax.set_title("Shipments by Fulfillment Type", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Fulfillment Type", fontsize=11)
    ax.set_ylabel("Number of Shipments", fontsize=11)
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)
    sns.despine()

    for bar in ax.patches:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{int(height):,}",
            ha="center", va="bottom", fontsize=10,
        )

    if created_internal_figure:
        plt.tight_layout()
        plt.show()


# ---------------------------------------------------------------------
# Combined dashboard
# ---------------------------------------------------------------------

def plot_shipment_dashboard(df: pd.DataFrame | None = None) -> None:
    """
    Combined dashboard with:
    1. Shipments by mode (top-left)
    2. Total value by mode (top-right)
    3. Shipments over time (middle, full width)
    4. Top countries by shipments (bottom-left)
    5. Fulfillment type comparison (bottom-right)
    """
    fig = plt.figure(figsize=(20, 16))

    gs = gridspec.GridSpec(
        3, 2,
        height_ratios=[1, 1, 1.2],
        hspace=0.55,
        wspace=0.42,
    )

    ax_mode_count = fig.add_subplot(gs[0, 0])
    ax_mode_value = fig.add_subplot(gs[0, 1])
    ax_time = fig.add_subplot(gs[1, :])
    ax_countries = fig.add_subplot(gs[2, 0])
    ax_fulfill = fig.add_subplot(gs[2, 1])

    plot_shipments_by_mode(df, pre_ax=ax_mode_count)
    plot_value_by_mode(df, pre_ax=ax_mode_value)
    plot_shipments_over_time(df, pre_ax=ax_time)
    plot_top_countries_by_shipments(df, top_n=10, pre_ax=ax_countries)
    plot_fulfill_type_comparison(df, pre_ax=ax_fulfill)

    fig.suptitle(
        "Shipment Activity — Descriptive Summary",
        fontsize=20,
        fontweight="bold",
        y=0.98,
    )

    plt.show()


# ---------------------------------------------------------------------
# Main workflow
# ---------------------------------------------------------------------

def run_shipment_summary(
    df: pd.DataFrame | None = None,
    show_charts: bool = True,
) -> dict:
    """
    Run the full shipment descriptive analysis workflow.

    Args:
        df: Optional pre-loaded DataFrame. If None, the cleaned dataset is loaded.
        show_charts: If True, display the shipment dashboard.

    Returns:
        dict with keys:
            shipment_data, overview, by_mode, by_fulfill,
            over_time, top_countries
    """
    shipment_data = prepare_shipment_data(df)
    overview = get_shipment_overview(shipment_data)
    by_mode = summarize_by_shipment_mode(shipment_data)
    by_fulfill = summarize_by_fulfill_type(shipment_data)
    over_time = summarize_shipments_over_time(shipment_data)
    top_countries = get_top_countries_by_shipments(shipment_data)

    print("=== Shipment Overview ===")
    print(overview.T.to_string(header=False))

    print("\n=== Shipments by Mode ===")
    print(by_mode.to_string(index=False))

    print("\n=== Shipments by Fulfillment Type ===")
    print(by_fulfill.to_string(index=False))

    print("\n=== Shipments Over Time ===")
    print(over_time.to_string(index=False))

    print(f"\n=== Top {len(top_countries)} Countries by Shipments ===")
    print(top_countries.to_string(index=False))

    if show_charts:
        plot_shipment_dashboard(shipment_data)

    return {
        "shipment_data": shipment_data,
        "overview": overview,
        "by_mode": by_mode,
        "by_fulfill": by_fulfill,
        "over_time": over_time,
        "top_countries": top_countries,
    }
