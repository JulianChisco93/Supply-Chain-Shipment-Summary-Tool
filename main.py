import numpy as np
import pandas as pd

INPUT_PATH = "data/supply_delivery_history.csv"
OUTPUT_PATH = "data/supply_delivery_history_clean.csv"

SENTINEL_STRINGS = {"N/A", "TBD", "unknown", ""}

DATE_COLUMNS = [
    "Scheduled Delivery Date",
    "Delivered to Client Date",
    "Delivery Recorded Date",
]

DATE_FORMATS = [
    "%d-%b-%y",     # 2-Jun-06
    "%d-%b-%Y",     # 2-Jun-2006
    "%d/%m/%Y",     # 08/01/2007
    "%d %b %Y",     # 22 Nov 2007
    "%Y/%m/%d",     # 2013/04/16
    "%Y-%m-%d",     # 2006-06-02
]


def parse_date_column(series: pd.Series) -> pd.Series:
    """Try each known format in turn; fall back to pandas inference; unparseable → NaT."""
    result = pd.Series(pd.NaT, index=series.index)
    remaining_mask = pd.isna(result)

    for fmt in DATE_FORMATS:
        if not remaining_mask.any():
            break
        parsed = pd.to_datetime(
            series.where(remaining_mask),
            format=fmt,
            errors="coerce",
        )
        filled = parsed.notna()
        result = result.where(~filled, parsed)
        remaining_mask = result.isna() & series.notna()

    # Final pass with pandas inference for any stragglers
    if remaining_mask.any():
        parsed = pd.to_datetime(
            series.where(remaining_mask),
            dayfirst=True,
            errors="coerce",
        )
        filled = parsed.notna()
        result = result.where(~filled, parsed)

    return result


def clean_unit_price(series: pd.Series) -> pd.Series:
    """
    Handle Unit Price quirks:
      - Strip 'USD ' prefix: 'USD 0.12' → '0.12'
      - Convert accounting negatives: '(0.14)' → '-0.14'
    """
    s = series.astype(str)
    s = s.str.strip()
    s = s.str.replace(r"^\s*USD\s*", "", regex=True)
    paren_mask = s.str.match(r"^\([\d.]+\)$")
    s = s.where(~paren_mask, "-" + s.str.strip("()"))
    return pd.to_numeric(s, errors="coerce")


def clean_line_item_quantity(series: pd.Series) -> pd.Series:
    """
    Handle Line Item Quantity quirks:
      - Remove commas: '1,447' → '1447'
      - Strip trailing ' units': '10240 units' → '10240'
    """
    s = series.astype(str).str.strip()
    s = s.str.replace(",", "", regex=False)
    s = s.str.replace(r"\s*units?\s*$", "", regex=True)
    return pd.to_numeric(s, errors="coerce")


def strip_all_strings(df: pd.DataFrame) -> pd.DataFrame:
    """Strip leading/trailing whitespace from every string column, regardless of dtype."""
    return df.apply(lambda col: col.str.strip() if col.dtype == object else col)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    # --- Step 1: Replace sentinel strings with NaN globally ---
    df = df.replace(list(SENTINEL_STRINGS), np.nan)

    # --- Step 2: Strip whitespace from ALL string columns ---
    df = strip_all_strings(df)

    # --- Step 3: Strip #<digits>** junk prefix from Item Description ---
    df["Item Description"] = (
        df["Item Description"]
        .str.replace(r"^#\d+\*+\s*", "", regex=True)
        .str.strip()
    )

    # --- Step 4: Normalize categorical casing ---
    # Inline strip before casing guarantees whitespace is gone even if step 2 missed any
    df["Product Group"] = df["Product Group"].str.strip().str.upper()
    df["Shipment Mode"] = df["Shipment Mode"].str.strip().str.title()
    df["Sub Classification"] = df["Sub Classification"].str.strip().str.title()
    df["Country"] = df["Country"].str.strip().str.title()
    df["First Line Designation"] = df["First Line Designation"].str.strip().str.title()
    df["Vendor"] = df["Vendor"].str.strip()
    df["Brand"] = df["Brand"].str.strip()
    df["Dosage Form"] = df["Dosage Form"].str.strip()
    df["Manufacturing Site"] = df["Manufacturing Site"].str.strip()
    df["Fulfill Via"] = df["Fulfill Via"].str.strip()

    # --- Step 5: Strip "USD " prefix from Line Item Value and Pack Price → float ---
    for col in ("Line Item Value", "Pack Price"):
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.replace(r"^\s*USD\s*", "", regex=True)
            .pipe(pd.to_numeric, errors="coerce")
        )

    # --- Step 6: Clean Line Item Quantity (commas, "units" suffix) → float ---
    df["Line Item Quantity"] = clean_line_item_quantity(df["Line Item Quantity"])

    # --- Step 7: Clean Unit Price (USD prefix, parentheses-as-negative) → float ---
    df["Unit Price"] = clean_unit_price(df["Unit Price"])

    # --- Step 8: Coerce Weight, Freight Cost, Unit of Measure → float ---
    for col in ("Weight (Kilograms)", "Freight Cost (USD)",
                "Unit of Measure (Per Pack)"):
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Also coerce Line Item Insurance which may have residual non-numeric values
    df["Line Item Insurance (USD)"] = pd.to_numeric(
        df["Line Item Insurance (USD)"], errors="coerce"
    )

    # --- Step 9: Parse and standardize all three date columns to YYYY-MM-DD ---
    for col in DATE_COLUMNS:
        parsed = parse_date_column(df[col].astype(str).replace("nan", np.nan))
        df[col] = parsed.dt.strftime("%Y-%m-%d").where(parsed.notna(), other=np.nan)

    return df


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
