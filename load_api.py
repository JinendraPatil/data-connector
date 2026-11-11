import time
import requests
import pandas as pd
from db import engine
from cleaning import clean_crypto

url = "https://api.coingecko.com/api/v3/coins/markets"
params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 50, "page": 1}

raw = None
for attempt in range(1, 4):                    # try up to 3 times
    try:
        response = requests.get(url, params=params, timeout=10)
        print("Status code:", response.status_code)
        response.raise_for_status()            # error if 4xx or 5xx
        raw = pd.DataFrame(response.json())
        break
    except requests.RequestException as e:
        print(f"Attempt {attempt} failed: {e}")
        time.sleep(2 * attempt)                # wait longer each time

if raw is None:
    raise RuntimeError("API failed after 3 attempts")

clean = clean_crypto(raw)
clean.to_sql("crypto_prices", engine, if_exists="replace", index=False)
print("Loaded", len(clean), "rows")