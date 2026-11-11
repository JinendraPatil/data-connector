import json
import pandas as pd
from db import engine
from cleaning import clean_customers

with open("data/customers.json", encoding="utf-8") as f:
    data = json.load(f)

raw = pd.json_normalize(data)     # flattens address -> address.city
print("Rows read:", len(raw))

clean = clean_customers(raw)
print("Rows after cleaning:", len(clean))

clean.to_sql("customers", engine, if_exists="replace", index=False)
print("Loaded into Postgres")