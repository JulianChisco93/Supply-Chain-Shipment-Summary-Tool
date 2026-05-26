"""
vendor_analysis.py
"""

# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt

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

