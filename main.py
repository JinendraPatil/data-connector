import json
import logging
import time
import pandas as pd
import requests
from db import engine
from cleaning import (clean_superstore, validate_superstore,
                      clean_customers, clean_crypto)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler("pipeline.log"), logging.StreamHandler()],
)


def run_superstore():
    raw = pd.read_csv("data/superstore.csv")
    df = clean_superstore(raw)
    problems = validate_superstore(df)
    if problems:
        raise ValueError(f"Data quality check failed: {problems}")
    df.to_sql("superstore_sales", engine, if_exists="replace", index=False, chunksize=1000)
    logging.info("superstore: read %d, loaded %d", len(raw), len(df))


def run_customers():
    with open("data/customers.json", encoding="utf-8") as f:
        raw = pd.json_normalize(json.load(f))
    df = clean_customers(raw)
    df.to_sql("customers", engine, if_exists="replace", index=False)
    logging.info("customers: read %d, loaded %d", len(raw), len(df))


def fetch_crypto():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 50, "page": 1}
    for attempt in range(1, 4):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return pd.DataFrame(response.json())
        except requests.RequestException as e:
            logging.warning("API attempt %d failed: %s", attempt, e)
            time.sleep(2 * attempt)
    raise RuntimeError("API failed after 3 attempts")


def run_crypto():
    raw = fetch_crypto()
    df = clean_crypto(raw)
    df.to_sql("crypto_prices", engine, if_exists="replace", index=False)
    logging.info("crypto: read %d, loaded %d", len(raw), len(df))


if __name__ == "__main__":
    for job in [run_superstore, run_customers, run_crypto]:
        try:
            job()
        except Exception:
            logging.exception("%s FAILED", job.__name__)   # one failure doesn't stop the others