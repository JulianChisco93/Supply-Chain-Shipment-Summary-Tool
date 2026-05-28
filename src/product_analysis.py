"""
product_analysis.py
"""

# ---------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt

from src.data_loader import load_clean_data


# ---------------------------------------------------------------------
# Functions to prepare product-related data
# ---------------------------------------------------------------------

def load_product_dataset() -> pd.DataFrame:
    """
    Load cleaned dataset.
    """
    return load_clean_data()


def prepare_product_data(df: pd.DataFrame | None = None) -> pd.DataFrame:
    """
    Prepare product-related dataset for analysis.
    """

    if df is None:
        df = load_product_dataset()

    product_df = df.copy()

    # Relevant columns
    required_columns = [
        "Product Group",
        "Sub Classification",
        "Item Description",
        "Dosage Form",
        "Brand",
        "Line Item Quantity",
        "Line Item Value"
    ]

    available_columns = [
        col for col in required_columns
        if col in product_df.columns
    ]

    product_df = product_df[available_columns].copy()

    # Standardize categorical columns
    categorical_columns = [
        "Product Group",
        "Sub Classification",
        "Dosage Form",
        "Brand"
    ]

    for column in categorical_columns:

        if column in product_df.columns:

            product_df[column] = (
                product_df[column]
                .astype(str)
                .str.strip()
                .str.upper()
            )

    # Convert numeric columns
    numeric_columns = [
        "Line Item Quantity",
        "Line Item Value"
    ]

    for column in numeric_columns:

        if column in product_df.columns:

            product_df[column] = pd.to_numeric(
                product_df[column],
                errors="coerce"
            ).fillna(0)

    return product_df


# ---------------------------------------------------------------------
# Functions to generate product insights
# ---------------------------------------------------------------------

def summarize_category(
    df: pd.DataFrame,
    category_column: str
) -> pd.DataFrame:
    """
    Generate shipment summaries by category.
    """

    summary = (
        df.groupby(category_column, as_index=False)
        .agg(
            Total_Line_Item_Quantity=(
                "Line Item Quantity",
                "sum"
            ),
            Total_Line_Item_Value=(
                "Line Item Value",
                "sum"
            )
        )
    )

    summary = summary.sort_values(
        by="Total_Line_Item_Value",
        ascending=False
    ).reset_index(drop=True)

    return summary


def get_top_products(
    df: pd.DataFrame,
    top_n: int = 10
) -> pd.DataFrame:
    """
    Return top products by shipment quantity.
    """

    top_products = (
        df.groupby("Item Description", as_index=False)
        .agg(
            Total_Line_Item_Quantity=(
                "Line Item Quantity",
                "sum"
            )
        )
    )

    top_products = top_products.sort_values(
        by="Total_Line_Item_Quantity",
        ascending=False
    ).head(top_n)

    return top_products


# ---------------------------------------------------------------------
# Visualization functions
# ---------------------------------------------------------------------

def plot_category_distribution(
    df: pd.DataFrame,
    category_column: str,
    top_n: int = 10
):
    """
    Plot category distribution.
    """

    distribution = (
        df[category_column]
        .value_counts()
        .head(top_n)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.barh(
        distribution.index.astype(str),
        distribution.values
    )

    ax.set_title(
        f"{category_column} Distribution"
    )

    ax.set_xlabel("Count")
    ax.set_ylabel(category_column)

    plt.tight_layout()

    return fig


# ---------------------------------------------------------------------
# Main product workflow
# ---------------------------------------------------------------------

def run_product_analysis(
    dataset=None,
    show_charts: bool = True
) -> dict:
    """
    Run complete product analysis workflow.
    """

    if dataset is None:
        product_data = prepare_product_data()
    else:
        product_data = prepare_product_data(dataset)

    product_summary = summarize_category(
        product_data,
        "Product Group"
    )

    subclassification_summary = summarize_category(
        product_data,
        "Sub Classification"
    )

    top_products = get_top_products(
        product_data
    )

    print("\nProduct Group Summary:")
    print(product_summary.head())

    print("\nSub Classification Summary:")
    print(subclassification_summary.head())

    print("\nTop Products:")
    print(top_products.head())

    if show_charts:

        fig = plot_category_distribution(
            product_data,
            "Dosage Form"
        )

        fig.savefig(
            "dosage_form_distribution.png"
        )

    return {
        "product_data": product_data,
        "product_summary": product_summary,
        "subclassification_summary": subclassification_summary,
        "top_products": top_products
    }