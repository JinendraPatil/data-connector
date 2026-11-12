# Multi-Source Data Connector

This is a data engineering project I built in Python. It reads data from three sources (a CSV file, a JSON file and a REST API), cleans it, checks it, and loads it into a PostgreSQL database.

## Data Sources

- **Superstore sales (CSV):** about 10,000 rows of retail sales data
- **Customers (JSON):** a small file with nested address data
- **Crypto prices (REST API):** live market data from the CoinGecko API

## Tech Used

Python, pandas, SQLAlchemy, PostgreSQL, requests, pytest, Git

## Project Structure

```
data-connector/
├── data/              # superstore.csv and customers.json
├── tests/             # pytest tests
├── connectors.py      # one class for each source
├── cleaning.py        # cleaning and validation functions
├── db.py              # database connection
├── main.py            # runs the whole pipeline
└── requirements.txt
```

## How It Works

Each source follows the same three steps: extract, transform, load.

- **Superstore CSV:** renames columns, removes extra spaces, keeps postal codes as text so leading zeros are not lost, removes duplicate rows, and checks that sales, quantity and discount values are valid
- **Customers JSON:** flattens the nested address, fills missing emails with "unknown", and removes duplicates
- **Crypto API:** fetches the data, retries up to 3 times if the request fails, and drops rows with no price

## How to Run

1. Create and activate a virtual environment
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
2. Install the libraries
   ```
   pip install -r requirements.txt
   ```
3. Create a PostgreSQL database called `connector_db`
4. Create a `.env` file in the main folder with your database details
   ```
   DB_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/connector_db
   ```
5. Run the pipeline
   ```
   python main.py
   ```
6. Run the tests
   ```
   python -m pytest
   ```

## Design Choices

- Each source has its own class, so a new source can be added without changing the others
- Every load replaces the table, so running the pipeline twice does not create duplicate rows
- If one source fails, the others still run
- All runs are written to a log file, `pipeline.log`
- The database password is kept in `.env`, which is not uploaded to GitHub

## What Happens When Something Fails

- **No internet:** the API connector retries 3 times and then fails, while the CSV and JSON loads still finish
- **Missing file:** only that source fails, and the error is logged
- **Wrong database password:** the load fails and the error is written to `pipeline.log`
- **Invalid data (for example, negative sales):** the quality check stops the load

## What I Learned

- How to build a simple ETL pipeline from scratch
- Cleaning data with pandas and loading it into PostgreSQL
- Handling API failures with retries and logging
- Writing unit tests for data cleaning code
- Using Git and GitHub

