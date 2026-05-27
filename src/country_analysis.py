import pandas as pd

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
