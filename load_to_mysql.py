
import os
from pathlib import Path

import pandas as pd
import mysql.connector

# Locate the processed CSV
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "processed_data" / "state_transactions.csv"

# Read the real dataset
df = pd.read_csv(CSV_PATH)

print("Records in CSV:", len(df))

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.environ["PAYPULSE_DB_PASSWORD"],
    database="paypulse_real"
)

cursor = connection.cursor()

# Insert records without creating duplicates
query = """
INSERT INTO state_transactions
(year, quarter, state, transaction_count, transaction_amount)
VALUES (%s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
transaction_count = VALUES(transaction_count),
transaction_amount = VALUES(transaction_amount)
"""

records = [
    (
        int(row.year),
        int(row.quarter),
        str(row.state),
        int(row.transaction_count),
        round(float(row.transaction_amount), 2)
    )
    for row in df.itertuples(index=False)
]

try:
    cursor.executemany(query, records)
    connection.commit()

    cursor.execute(
        "SELECT COUNT(*) FROM state_transactions"
    )

    print("Records in MySQL:", cursor.fetchone()[0])
    print("Import completed successfully!")

except mysql.connector.Error as error:
    connection.rollback()
    print("Import failed:", error)

finally:
    cursor.close()
    connection.close()
