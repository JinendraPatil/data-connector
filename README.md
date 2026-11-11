# Multi-Source Data Connector

A Python ETL pipeline that ingests data from a CSV file, a JSON file, and a
REST API, cleans and validates it, and loads it into PostgreSQL.

## Architecture

CSV (Superstore, ~10K rows) ─┐
JSON (customers)             ├─> Connectors (extract -> clean -> validate) ─> PostgreSQL
REST API (CoinGecko)         ─┘

[Add a diagram image here, drawn at excalidraw.com]

## Tech Stack

Python, pandas, SQLAlchemy, PostgreSQL, requests, pytest

## How to Run

1. Create a virtual environment: `python -m venv venv` and activate it
2. Install libraries: `pip install -r requirements.txt`
3. Create a PostgreSQL database named `connector_db`
4. Create a `.env` file with:
   `DB_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/connector_db`
5. Run the pipeline: `python main.py`
6. Run the tests: `python -m pytest`

## What the Pipeline Does

- **Superstore CSV:** renames columns, trims spaces, keeps postal codes as text,
  removes duplicate rows, validates sales, quantity and discount
- **Customers JSON:** flattens nested address, fills missing emails, removes duplicates
- **Crypto API:** fetches market data with retry and backoff, drops rows with no price

## Design Decisions

- One class per source, sharing a `BaseConnector` with extract, transform, load
- Loads use `replace`, so running the pipeline twice gives the same result (idempotent)
- One failing source does not stop the others
- All runs are logged to `pipeline.log`
- Credentials are stored in `.env` and never committed

## Failure Scenarios Tested

| Scenario | Behaviour |
|---|---|
| No internet | [write what you saw] |
| Missing JSON file | [write what you saw] |
| Wrong database password | [write what you saw] |
| Invalid sales value | [write what you saw] |

## Future Improvements

- Incremental loads instead of full replace
- Orchestration with Airflow
- Docker and CI with GitHub Actions