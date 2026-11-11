import pandas as pd
from cleaning import (clean_superstore, validate_superstore,
                      clean_customers, clean_crypto)


def make_sample():
    return pd.DataFrame({
        "Ship Mode": [" Second Class", "Second Class", "First Class"],
        "Segment": ["Consumer", "Consumer", "Corporate"],
        "Country": ["United States"] * 3,
        "City": ["Henderson", "Henderson", "Boston"],
        "State": ["Kentucky", "Kentucky", "Massachusetts"],
        "Postal Code": [42420, 42420, 1040],
        "Region": ["South", "South", "East"],
        "Category": ["Furniture", "Furniture", "Technology"],
        "Sub-Category": ["Chairs", "Chairs", "Phones"],
        "Sales": [100.0, 100.0, 50.0],
        "Quantity": [2, 2, 1],
        "Discount": [0.0, 0.0, 0.2],
        "Profit": [10.0, 10.0, -5.0],
    })


def test_removes_duplicates_and_trims_spaces():
    out = clean_superstore(make_sample())
    assert len(out) == 2
    assert out.iloc[0]["ship_mode"] == "Second Class"


def test_postal_code_keeps_leading_zero():
    out = clean_superstore(make_sample())
    assert "01040" in out["postal_code"].values


def test_validation_catches_bad_discount():
    out = clean_superstore(make_sample())
    out.loc[0, "discount"] = 5
    assert "Discount must be between 0 and 1" in validate_superstore(out)


def test_customers_fill_email_and_remove_duplicates():
    df = pd.DataFrame({
        "customer_id": [1, 1, 2],
        "name": ["A", "A", "B"],
        "email": [None, None, "b@x.com"],
        "address.city": ["Pune", "Pune", "Mumbai"],
    })
    out = clean_customers(df)
    assert len(out) == 2
    assert out.iloc[0]["email"] == "unknown"
    assert out.iloc[0]["city"] == "Pune"


def test_crypto_drops_missing_price():
    df = pd.DataFrame({
        "id": ["bitcoin", "ghost"],
        "symbol": ["btc", "gh"],
        "name": ["Bitcoin", "Ghost"],
        "current_price": [100.0, None],
        "market_cap": [1000, 5],
    })
    out = clean_crypto(df)
    assert len(out) == 1
    assert out.iloc[0]["coin_id"] == "bitcoin"