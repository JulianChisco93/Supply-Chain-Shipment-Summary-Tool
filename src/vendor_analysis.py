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

