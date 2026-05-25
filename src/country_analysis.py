import pandas as pd

df = pd.read_csv("supply_delivery_history.csv")
print(df.columns)
print(df.head())

print(df.info())

def summarize_by_country(df):
    pass

def shipments_count_by_country(df):
    pass