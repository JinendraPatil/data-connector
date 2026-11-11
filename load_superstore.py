import pandas as pd
from db import engine
from cleaning import clean_superstore, validate_superstore

# Extract
raw = pd.read_csv("data/superstore.csv")
print("Rows read:", len(raw))

# Transform
clean = clean_superstore(raw)
print("Rows after cleaning:", len(clean))

# Validate
problems = validate_superstore(clean)
if problems:
    raise ValueError(f"Data quality check failed: {problems}")
print("All checks passed")

# Load
clean.to_sql("superstore_sales", engine, if_exists="replace", index=False, chunksize=1000)
print("Loaded into Postgres")