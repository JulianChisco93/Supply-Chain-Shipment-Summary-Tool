import pandas as pd
import matplotlib.pyplot as plt

from src.cleaning import DATE_COLUMNS, clean
from src.vendor_analysis import run_vendor_analysis
from src.country_analysis import run_country_analysis
from src.product_analysis import run_product_analysis
from src.shipment_summary import run_shipment_summary


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


    # country analysis
    print("---------------------------------------------------------------------")
    print("\n--- Country analysis ---")
    print("---------------------------------------------------------------------")
    run_country_analysis(df_clean)

    # product analysis
    print("---------------------------------------------------------------------")
    print("\n--- Product analysis ---")
    print("---------------------------------------------------------------------")
    run_product_analysis(df_clean)

    # vendor analysis
    print("---------------------------------------------------------------------")
    print("\n--- Vendor analysis ---")
    print("---------------------------------------------------------------------")
    run_vendor_analysis(df_clean)

    # shipment analysis
    print("---------------------------------------------------------------------")
    print("\n--- Shipment analysis ---")
    print("---------------------------------------------------------------------")
    run_shipment_summary(df_clean)

    # show plots at the end
    plt.show()


if __name__ == "__main__":
    main()
