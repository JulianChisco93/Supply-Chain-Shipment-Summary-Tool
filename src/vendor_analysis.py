"""
vendor_analysis.py
"""

# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt

from src.data_loader import load_clean_data

from pathlib import Path


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
