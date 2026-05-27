import pandas as pd

df = pd.read_csv("supply_delivery_history_clean.csv")
#df = pd.read_csv("supply_delivery_history.csv")
print(df.columns)
print(df.head())

print(df.info())

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

def summarize_by_country(df):
    """
    Returns total quantity and value per country.
    """


