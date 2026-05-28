import pandas as pd

from src.cleaning import DATE_COLUMNS, clean

INPUT_PATH = "data/supply_delivery_history.csv"
OUTPUT_PATH = "data/supply_delivery_history_clean.csv"


def main():
    df = pd.read_csv(INPUT_PATH, dtype=str)
    print(f"Loaded {len(df):,} rows x {len(df.columns)} columns")

    df_clean = clean(df)

    # --- Summary report ---
    print("\n--- Cleaning summary ---")

    print("\nDate columns (NaT count):")
    for col in DATE_COLUMNS:
        print(f"  {col}: {df_clean[col].isna().sum()} unparseable/missing")

    print("\nNumeric columns (NaN count):")
    for col in ("Line Item Quantity", "Line Item Value", "Pack Price", "Unit Price",
                "Weight (Kilograms)", "Freight Cost (USD)", "Line Item Insurance (USD)"):
        print(f"  {col}: {df_clean[col].isna().sum()} NaN")

    print("\nCategorical unique values:")
    for col in ("Product Group", "Shipment Mode", "Sub Classification",
                "First Line Designation", "Fulfill Via"):
        print(f"  {col}: {sorted(df_clean[col].dropna().unique())}")

    print(f"\n  Country: {df_clean['Country'].nunique()} unique values")
    print(f"  Country list: {sorted(df_clean['Country'].dropna().unique())}")

    df_clean.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved cleaned dataset → {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
