import pandas as pd

df = pd.read_csv("supply_delivery_history.csv")
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


import pandas as pd

df = pd.read_csv("supply_delivery_history_clean.csv")

print(summarize_by_country(df).head(10))
print(shipments_count_by_country(df).head(10))