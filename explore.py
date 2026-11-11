import pandas as pd

df = pd.read_csv("data/superstore.csv")

print(df.shape)                      # (rows, columns)
print(df.head())                     # first 5 rows
print(df.dtypes)                     # type of each column
print(df.isnull().sum())             # blanks per column
print("Duplicate rows:", df.duplicated().sum())