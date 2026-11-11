import pandas as pd


def clean_superstore(df):
    df = df.copy()

    # 1. Make column names SQL-friendly: "Ship Mode" -> "ship_mode"
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # 2. Remove extra spaces from text columns
    text_cols = ["ship_mode", "segment", "country", "city",
                 "state", "region", "category", "sub_category"]
    for col in text_cols:
        df[col] = df[col].str.strip()

    # 3. Keep postal codes as 5-character text so 1040 becomes "01040"
    df["postal_code"] = df["postal_code"].astype(str).str.zfill(5)

    # 4. Remove exact duplicate rows
    df = df.drop_duplicates()

    return df

def validate_superstore(df):
    problems = []
    if df.isnull().any().any():
        problems.append("Found null values")
    if not (df["sales"] > 0).all():
        problems.append("Sales must be greater than 0")
    if not (df["quantity"] > 0).all():
        problems.append("Quantity must be greater than 0")
    if not df["discount"].between(0, 1).all():
        problems.append("Discount must be between 0 and 1")
    return problems

def clean_customers(df):
    df = df.rename(columns={"address.city": "city"})
    df = df[["customer_id", "name", "email", "city"]].copy()
    df["email"] = df["email"].fillna("unknown")
    return df.drop_duplicates(subset="customer_id")


def clean_crypto(df):
    df = df[["id", "symbol", "name", "current_price", "market_cap"]].copy()
    df = df.rename(columns={"id": "coin_id"})
    df = df.dropna(subset=["coin_id", "current_price"])
    return df.drop_duplicates(subset="coin_id")