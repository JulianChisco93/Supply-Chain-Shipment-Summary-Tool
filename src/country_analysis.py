import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# NOTE:
# This module assumes that the dataset has already been cleaned.

def summarize_by_country(df):
    return df.groupby("Country").agg({
        "Line Item Quantity": "sum",
        "Line Item Value": "sum"
    }).reset_index()

def shipments_count_by_country(df):
    return df.groupby("Country").size().reset_index(name="Total Shipments")

def top_countries_by_value(df, top_n=10):
    summary = summarize_by_country(df)
    return summary.sort_values(by="Line Item Value", ascending=False).head(top_n)

def shipment_mode_by_country(df):
    return df.groupby(["Country", "Shipment Mode"]).size().reset_index(name="Count")


def plot_top_countries_by_revenue(df, top_n=10):
    """
    Plot the top countries by revenue using Line Item Value.
    """

    top_countries = top_countries_by_value(df, top_n).copy()

    top_countries = top_countries.sort_values(
        by="Line Item Value",
        ascending=True
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.barh(
        top_countries["Country"],
        top_countries["Line Item Value"]
    )

    ax.set_title(
        f"Top {top_n} Countries by Revenue"
    )

    ax.set_xlabel("Revenue")
    ax.set_ylabel("Country")

    ax.xaxis.set_major_formatter(
        mtick.FuncFormatter(lambda x, _: f"${x/1_000_000:,.1f}M")
    )

    for i, value in enumerate(top_countries["Line Item Value"]):
        ax.text(
            value,
            i,
            f"${value/1_000_000:,.1f}M",
            va="center",
            ha="left",
            fontsize=9
        )

    plt.tight_layout()

    return fig


def run_country_analysis(df):
    """
    Run the country-level analysis and print the results
    """

    print("\nSummary by country:")
    print(summarize_by_country(df).head(10))

    print("\nShipments count by country:")
    print(shipments_count_by_country(df).head(10))

    print("\nTop countries by value:")
    print(top_countries_by_value(df).head(10))

    print("\nShipment mode by country:")
    print(shipment_mode_by_country(df).head(10))


    fig = plot_top_countries_by_revenue(df, top_n=10)
    # plt.show()