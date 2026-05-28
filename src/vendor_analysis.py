"""
vendor_analysis.py
"""

# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.gridspec as gridspec
import seaborn as sns

from src.data_loader import load_clean_data

from pathlib import Path


# ---------------------------------------------------------------------
# Functions to prepare data for vendor analysis
# ---------------------------------------------------------------------
# function to load the cleaned dataset
def load_vendor_dataset() -> pd.DataFrame:
    """
    Load the cleaned dataset
    Returns:
        pd.DataFrame
    """
    df = load_clean_data()
    return df

# function to convert text columna to numberical values
def clean_numeric_value(series: pd.Series) -> pd.Series:
    """
    Convert a text-based numeric column into numeric format.
    Returns:
        pd.Series: Numeric column.
    """
    return (
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.replace("USD", "", regex=False)
        .str.replace("usd", "", regex=False)
        .str.replace("units", "", regex=False)
        .str.replace("unit", "", regex=False)
        .str.replace("N/A", "0", regex=False)
        .str.replace("n/a", "0", regex=False)
        .str.strip()
        .replace({"": "0", "nan": "0", "None": "0"})
        .pipe(pd.to_numeric, errors="coerce")
        .fillna(0)
    )


# function to get a dataframe with only the vendor information
def prepare_vendor_data(df: pd.DataFrame | None = None) -> pd.DataFrame:
    """
    Select and prepare vendor-related data for analysis.
    Returns:
        pd.DataFrame: Prepared vendor-level dataset.
    """
    if df is None:
        df = load_vendor_dataset()

    vendor_df = df.copy()

    # Remove duplicated records
    vendor_df = vendor_df.drop_duplicates()

    # Relevant columns for vendor analysis
    required_columns = [
        "ID",
        "Vendor",
        "Unit of Measure (Per Pack)",
        "Line Item Quantity",
        "Line Item Value",
        "Pack Price",
        "Unit Price",
    ]

    # Keep only columns that exist in the dataset
    available_columns = [col for col in required_columns if col in vendor_df.columns]
    vendor_df = vendor_df[available_columns].copy()

    # Standardize vendor names
    if "Vendor" in vendor_df.columns:
        vendor_df["Vendor"] = (
            vendor_df["Vendor"]
            .astype(str)
            .str.strip()
            .str.upper()
            .replace({"": "UNKNOWN", "NAN": "UNKNOWN", "NONE": "UNKNOWN"})
        )

    # Convert numeric fields
    numeric_columns = [
        "Unit of Measure (Per Pack)",
        "Line Item Quantity",
        "Line Item Value",
        "Pack Price",
        "Unit Price",
    ]

    for column in numeric_columns:
        if column in vendor_df.columns:
            vendor_df[column] = clean_numeric_value(vendor_df[column])   

    return vendor_df



# ---------------------------------------------------------------------
# Functions to show insights about vendors
# ---------------------------------------------------------------------
#function to show the summary of the vendor dataset
def get_vendor_summary(df: pd.DataFrame | None = None) -> pd.DataFrame:
    """
    Create a vendor-level summary.
    Returns:
        pd.DataFrame: Vendor summary sorted by revenue descending.
    """
    vendor_df = prepare_vendor_data(df)

    summary = (
        vendor_df
        .groupby("Vendor", as_index=False)
        .agg(
            Shipment_Records=("ID", "count"),
            Total_Line_Item_Quantity=("Line Item Quantity", "sum"),
            Total_Line_Item_Value=("Line Item Value", "sum"),
            Average_Pack_Price=("Pack Price", "mean"),
            Average_Unit_Price=("Unit Price", "mean"),
        )
    )

    summary = summary.sort_values(
        by="Total_Line_Item_Value",
        ascending=False
    ).reset_index(drop=True)

    return summary


# function to select top n vendors by revenue
def get_top_vendors_by_revenue(
    df: pd.DataFrame | None = None,
    top_n: int = 5
) -> pd.DataFrame:
    """
    Return the top vendors by total line item value.
    Returns:
        pd.DataFrame: Top vendors by revenue.
    """
    summary = get_vendor_summary(df)
    return summary.head(top_n)

# function to select bottom n vendors by revenue
def get_bottom_vendors_by_revenue(
    df: pd.DataFrame | None = None,
    bottom_n: int = 5
) -> pd.DataFrame:
    """
    Return the bottom vendors by total line item value
    Returns:
        pd.DataFrame: Bottom vendors by revenue.
    """
    summary = get_vendor_summary(df)

    summary = summary[
        (summary["Total_Line_Item_Value"] > 0)
        & (summary["Vendor"] != "UNKNOWN")
    ]

    return summary.tail(bottom_n).sort_values(
        by="Total_Line_Item_Value",
        ascending=True
    ).reset_index(drop=True)



# ---------------------------------------------------------------------
# Functions to show Visualizations about vendors
# ---------------------------------------------------------------------
#function to plot the total line item value for the top vendors
def plot_vendor_revenue(
    df: pd.DataFrame | None = None,
    top_n: int = 10
) -> None:
    """
    Plot the total line item value for the top vendors.
    """
    summary = get_vendor_summary(df)
    top_vendors = summary.head(top_n)

    plt.figure(figsize=(12, 6))
    plt.bar(top_vendors["Vendor"], top_vendors["Total_Line_Item_Value"], color="skyblue")
    plt.xlabel("Vendor")
    plt.ylabel("Total Line Item Value (Revenue)")
    plt.title(f"Top {top_n} Vendors by Revenue")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


#function to plot the total line item quantity for the top vendors
def plot_vendor_quantity(
    df: pd.DataFrame | None = None,
    top_n: int = 10
) -> None:
    """
    Plot the total line item quantity for the top vendors.
    """
    summary = get_vendor_summary(df)
    top_vendors = summary.head(top_n)

    plt.figure(figsize=(12, 6))
    plt.bar(top_vendors["Vendor"], top_vendors["Total_Line_Item_Quantity"], color="salmon")
    plt.xlabel("Vendor")
    plt.ylabel("Total Line Item Quantity")
    plt.title(f"Top {top_n} Vendors by Quantity")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


# function to plot the total line item value (in bars) for the top vendors and the total line item quantity (in line) for the same vendors
def plot_vendor_revenue_and_quantity(
    df: pd.DataFrame | None = None,
    top_n: int = 10
) -> None:
    """
    Plot the total line item value (in bars) for the top vendors and the total line item quantity (in line) for the same vendors.
    """
    summary = get_vendor_summary(df)
    top_vendors = summary.head(top_n)

    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.bar(top_vendors["Vendor"], top_vendors["Total_Line_Item_Value"], color="skyblue")
    ax1.set_xlabel("Vendor")
    ax1.set_ylabel("Total Line Item Value (Revenue)", color="skyblue")
    ax1.tick_params(axis="y", labelcolor="skyblue")
    ax1.set_title(f"Top {top_n} Vendors by Revenue and Quantity")
    ax1.set_xticklabels(top_vendors["Vendor"], rotation=45, ha="right")

    ax2 = ax1.twinx()
    ax2.plot(top_vendors["Vendor"], top_vendors["Total_Line_Item_Quantity"], color="salmon", marker="o")
    ax2.set_ylabel("Total Line Item Quantity", color="salmon")
    ax2.tick_params(axis="y", labelcolor="salmon")

    plt.tight_layout()
    plt.show()

# function to improve the previous plot by adding labels, formatting the y-axis, and improving the title and x-axis labels
def plot_vendor_revenue_and_quantity_improved(df, top_n=10, pre_ax=None):
    """
    Plot Revenue as bars and Quantity as line for the top vendors by revenue.
    """

    summary = get_vendor_summary(df)
    top_vendors = summary.head(top_n).copy()

    # Shorten vendor names if they are too long for better visualization
    top_vendors["Vendor"] = top_vendors["Vendor"].apply(
        lambda x: x[:30] + "..." if len(x) > 30 else x
    )

    # fig, ax1 = plt.subplots(figsize=(14, 7))

    created_internal_figure = False

    if pre_ax is None:
        fig, ax1 = plt.subplots(figsize=(14, 7))
        created_internal_figure = True
    else:
        ax1 = pre_ax


    # Bar chart: Revenue
    bars = ax1.bar(
        top_vendors["Vendor"],
        top_vendors["Total_Line_Item_Value"],
        color="#4FA3D1",
        alpha=0.85,
        label="Revenue"
    )

    ax1.set_xlabel("Vendor")
    ax1.set_ylabel("Revenue", color="#4FA3D1", fontsize=11)
    ax1.tick_params(axis="y", labelcolor="#4FA3D1")

    # Format left Y-axis as currency in millions
    ax1.yaxis.set_major_formatter(
        mtick.FuncFormatter(lambda x, _: f"${x/1_000_000:,.1f}M")
    )

    # Add revenue labels on bars
    for bar in bars:
        height = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"${height/1_000_000:,.1f}M",
            ha="center",
            va="bottom",
            fontsize=9,
            rotation=0
        )

    # Line chart: Quantity
    ax2 = ax1.twinx()

    ax2.plot(
        top_vendors["Vendor"],
        top_vendors["Total_Line_Item_Quantity"],
        color="#E76F51",
        marker="o",
        linewidth=2.5,
        label="Quantity"
    )

    ax2.set_ylabel("Quantity", color="#E76F51", fontsize=11)
    ax2.tick_params(axis="y", labelcolor="#E76F51")

    # Format right Y-axis in thousands/millions
    ax2.yaxis.set_major_formatter(
        mtick.FuncFormatter(lambda x, _: f"{x/1_000_000:,.1f}M")
    )

    # Title
    # plt.title(
    ax1.set_title(
        f"Top {top_n} Vendors by Revenue and Quantity",
        fontsize=15,
        fontweight="bold",
        pad=15
    )

    # Improve X labels
    ax1.set_xticks(range(len(top_vendors["Vendor"])))
    ax1.set_xticklabels(
        top_vendors["Vendor"],
        rotation=45,
        ha="right",
        fontsize=9
    )

    # Grid only for revenue axis
    ax1.grid(axis="y", linestyle="--", alpha=0.3)
    ax1.set_axisbelow(True)

    # Add combined legend
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(
        lines_1 + lines_2,
        labels_1 + labels_2,
        loc="upper right",
        frameon=True
    )

    # ONLY SHOW IF STANDALONE    
    if created_internal_figure:
        plt.tight_layout()
        plt.show()



# function to plot top 5 vendors by revenue in horizontal bars
def plot_top_vendors_by_revenue_horizontal(df, top_n=5, pre_ax=None):
    """
    Plot the top vendors by revenue in horizontal bars.
    """
    summary = get_vendor_summary(df)
    top_vendors = summary.head(top_n).copy()

    # Shorten vendor names if they are too long for better visualization
    top_vendors["Vendor"] = top_vendors["Vendor"].apply(
        lambda x: x[:30] + "..." if len(x) > 30 else x
    )

    # Create figure
    # plt.figure(figsize=(14, 7))
    created_internal_figure = False

    if pre_ax is None:
        fig, ax = plt.subplots(figsize=(14, 7))
        created_internal_figure = True
    else:
        ax = pre_ax

    # Create horizontal bar chart
    ax = sns.barplot(
        x="Total_Line_Item_Value",
        y="Vendor",
        data=top_vendors,
        palette="Blues_r",
        ax = ax
    )

    # FORMAT X-AXIS AS CURRENCY
    ax.xaxis.set_major_formatter(
        mtick.FuncFormatter(lambda x, _: f'${x/1_000_000:,.0f}M')
    )

    # ADD VALUES TO BARS
    for i, value in enumerate(top_vendors["Total_Line_Item_Value"]):

        ax.text(
            value + (top_vendors["Total_Line_Item_Value"].max() * 0.01),
            i,
            f'${value/1_000_000:,.1f}M',
            va='center',
            fontsize=10,
            fontweight='bold',
            color='black'
        )

    # TITLES AND LABELS
    # plt.title(
    ax.set_title(
        f"Top {top_n} Vendors by Revenue",
        fontsize=16,
        fontweight='bold',
        pad=15
    )

    # plt.xlabel(
    ax.set_xlabel(
        "Revenue",
        fontsize=12
    )

    # plt.ylabel(
    ax.set_ylabel(
        "Vendor",
        fontsize=12
    )

    # IMPROVE STYLE
    ax.grid(
        axis='x',
        linestyle='--',
        alpha=0.3
    )

    ax.set_axisbelow(True)

    # Remove top/right borders
    sns.despine(left=False, bottom=False)

    if created_internal_figure:
        # Better spacing
        plt.tight_layout()

        # Show chart
        plt.show()


# function to plot bottom 5 vendors by revenue in horizontal bars
def plot_bottom_vendors_by_revenue_horizontal(df, bottom_n=5, pre_ax=None):
    """
    Plot the bottom vendors by revenue in horizontal bars.
    """
    summary = get_vendor_summary(df)

    summary = summary[
        (summary["Total_Line_Item_Value"] > 0)
        & (summary["Vendor"] != "UNKNOWN")
    ]

    bottom_vendors = summary.tail(bottom_n).copy()
    
    # Shorten vendor names if they are too long for better visualization
    bottom_vendors["Vendor"] = bottom_vendors["Vendor"].apply(
        lambda x: x[:30] + "..." if len(x) > 30 else x
    )

    # Create figure
    # plt.figure(figsize=(14, 7))
    created_internal_figure = False

    if pre_ax is None:
        fig, ax = plt.subplots(figsize=(14, 7))
        created_internal_figure = True
    else:
        ax = pre_ax

    # Create horizontal bar chart
    ax = sns.barplot(
        x="Total_Line_Item_Value",
        y="Vendor",
        data=bottom_vendors,
        palette="Reds_r",
        ax=ax
    )

    # FORMAT X-AXIS AS CURRENCY
    ax.xaxis.set_major_formatter(
        mtick.FuncFormatter(lambda x, _: f'${x/1_000_000:,.0f}M')
    )

    # ADD VALUES TO BARS
    for i, value in enumerate(bottom_vendors["Total_Line_Item_Value"]):

        ax.text(
            value + (bottom_vendors["Total_Line_Item_Value"].max() * 0.01),
            i,
            f'${value/1_000_000:,.1f}M',
            va='center',
            fontsize=10,
            fontweight='bold',
            color='black'
        )

    # TITLES AND LABELS
    # plt.title(
    ax.set_title(
        f"Bottom {bottom_n} Vendors by Revenue",
        fontsize=16,
        fontweight='bold',
        pad=15
    )

    # plt.xlabel(
    ax.set_xlabel(
        "Revenue",
        fontsize=12
    )

    # plt.ylabel(
    ax.set_ylabel(
        "Vendor",
        fontsize=12
    )

    # IMPROVE STYLE
    ax.grid(
        axis='x',
        linestyle='--',
        alpha=0.3
    )

    ax.set_axisbelow(True)

    # Remove top/right borders
    sns.despine(left=False, bottom=False)

    if created_internal_figure:
        # Better spacing
        plt.tight_layout()

        # Show chart
        plt.show()


# ---------------------------------------------------------------------
# Functions to make a combined figure like a dashboard with multiple vendor insights
# ---------------------------------------------------------------------
# function to create a dashboard with the previous graphs
def plot_vendor_dashboard(vendor_data, top_n=10, top_revenue_n=5, bottom_revenue_n=5):
    """
    Creates one dashboard with:
    1. Revenue and Quantity chart on the left
    2. Top vendors by revenue on the top-right
    3. Bottom vendors by revenue on the bottom-right
    """

    fig = plt.figure(figsize=(16, 7))

    gs = gridspec.GridSpec(
        2, 2,
        width_ratios=[1.95, 1],
        height_ratios=[1, 1],
        wspace=0.55,
        hspace=0.42
    )

    ax_left = fig.add_subplot(gs[:, 0])
    ax_top_right = fig.add_subplot(gs[0, 1])
    ax_bottom_right = fig.add_subplot(gs[1, 1])

    # Call your existing chart functions
    plot_vendor_revenue_and_quantity_improved(
        vendor_data,
        top_n=top_n,
        pre_ax=ax_left
    )

    plot_top_vendors_by_revenue_horizontal(
        vendor_data,
        top_n=top_revenue_n,
        pre_ax=ax_top_right
    )

    plot_bottom_vendors_by_revenue_horizontal(
        vendor_data,
        bottom_n=bottom_revenue_n,
        pre_ax=ax_bottom_right
    )

    fig.suptitle(
        "Vendor Revenue and Quantity Analysis",
        fontsize=18,
        fontweight="bold",
        y=0.99
    )

    fig.subplots_adjust(
        left=0.06,
        right=0.97,
        top=0.90,
        bottom=0.16,
        wspace=0.42,
        hspace=0.42
    )

    # plt.tight_layout()
    # plt.show()




# ---------------------------------------------------------------------
# Main vendor workflow to run the analysis and show the charts
# ---------------------------------------------------------------------
# function to run the vendor analysis workflow
def run_vendor_analysis(dataset=None, show_charts: bool = True) -> dict:
    """
    Run the vendor analysis workflow.

    Args:
        dataset: Optional dataset. If None, vendor data is prepared internally.
        show_charts (bool): If True, displays the vendor dashboard.

    Returns:
        dict: Dictionary containing vendor data and vendor summary.
    """

    # prepare vendor data (if not provided) and get summary
    if dataset is None:
        vendor_data = prepare_vendor_data()
    else:
        vendor_data = prepare_vendor_data(dataset)

    # get vendor summary
    vendor_summary = get_vendor_summary(vendor_data)

    print("\nVendor Summary:")
    print(vendor_summary.head(10))

    if show_charts:
        plot_vendor_dashboard(
            vendor_data,
            top_n=10,
            top_revenue_n=5,
            bottom_revenue_n=5
        )

    return {
        "vendor_data": vendor_data,
        "vendor_summary": vendor_summary
    }