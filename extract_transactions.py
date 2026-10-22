
import json
import pandas as pd
from pathlib import Path

# Project and dataset locations
BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = (
    BASE_DIR / "pulse-main" / "data"
    / "aggregated" / "transaction"
    / "country" / "india"
)

OUTPUT_DIR = BASE_DIR / "processed_data"
OUTPUT_DIR.mkdir(exist_ok=True)

records = []

# Read national data only
for year_dir in sorted(DATA_DIR.iterdir()):

    if not year_dir.is_dir():
        continue

    if not year_dir.name.isdigit():
        continue

    year = int(year_dir.name)

    for file_path in sorted(year_dir.glob("*.json")):

        quarter = int(file_path.stem)

        with open(
            file_path, "r", encoding="utf-8"
        ) as file:
            raw_data = json.load(file)

        categories = (
            raw_data.get("data", {})
            .get("transactionData") or []
        )

        for category in categories:

            for instrument in (
                category.get("paymentInstruments") or []
            ):

                if instrument.get("type") != "TOTAL":
                    continue

                records.append({
                    "year": year,
                    "quarter": quarter,
                    "category": category.get("name"),
                    "transaction_count": instrument.get("count"),
                    "transaction_amount": instrument.get("amount")
                })

# Create dataframe
df = pd.DataFrame(records)

# Basic validation
print("Total records extracted:", len(df))
print("\nAvailable columns:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())

print("\nSample records:")
print(df.head(10).to_string(index=False))

# Export to CSV
output_file = (
    OUTPUT_DIR / "national_transactions.csv"
)

df.to_csv(output_file, index=False)

print("\nCSV saved successfully!")
print("Location:", output_file)
