"""
data_loader.py
This module contains reusable functions to load the raw and cleaned Supply Chain Shipment dataset.
"""

# Import necessary libraries
from pathlib import Path
import pandas as pd

# Define the path to the data directory
RAW_DATA_PATH = Path("data/supply_delivery_history.csv")
CLEAN_DATA_PATH = Path("data/supply_delivery_history_clean.csv")


# Function to load the raw dataset
def load_raw_data(file_path: str | Path = RAW_DATA_PATH) -> pd.DataFrame:
    """
    Load the original raw shipment dataset.
    Parameters:
        file_path: Path to the raw CSV file.
    Returns:
        pandas DataFrame with raw shipment data.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Raw data file not found: {file_path}")

    return pd.read_csv(file_path)



# Function to load the cleaned dataset
def load_clean_data(file_path: str | Path = CLEAN_DATA_PATH) -> pd.DataFrame:
    """
    Load the cleaned shipment dataset.
    Parameters:
        file_path: Path to the cleaned CSV file.
    Returns:
        pandas DataFrame with cleaned shipment data.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Clean data file not found: {file_path}. "
            "Run the cleaning process first."
        )

    return pd.read_csv(file_path)