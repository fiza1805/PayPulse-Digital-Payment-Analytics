
import json
import pandas as pd
from pathlib import Path

# ==========================================
# PAYPULSE: REAL STATE TRANSACTION EXTRACTION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = (
    BASE_DIR / "pulse-main" / "data"
    / "map" / "transaction"
    / "hover" / "country" / "india"
)

OUTPUT_DIR = BASE_DIR / "processed_data"
OUTPUT_DIR.mkdir(exist_ok=True)

records = []

# Read yearly folders
for year_dir in sorted(DATA_DIR.iterdir()):

    if not year_dir.is_dir():
        continue

    if not year_dir.name.isdigit():
        continue

    year = int(year_dir.name)

    # Read quarterly JSON files
    for file_path in sorted(year_dir.glob("*.json")):

        quarter = int(file_path.stem)

        with open(
            file_path, "r", encoding="utf-8"
        ) as file:
            raw_data = json.load(file)

        locations = (
            raw_data.get("data", {})
            .get("hoverDataList") or []
        )

        for location in locations:

            state = location.get("name")

            for metric in location.get("metric", []):

                if metric.get("type") != "TOTAL":
                    continue

                records.append({
                    "year": year,
                    "quarter": quarter,
                    "state": state,
                    "transaction_count": metric.get("count"),
                    "transaction_amount": metric.get("amount")
                })

# Convert to DataFrame
df = pd.DataFrame(records)

print("Total records:", len(df))

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate state-quarter records:")
print(
    df.duplicated(
        subset=["year", "quarter", "state"]
    ).sum()
)

print("\nSample records:")
print(df.head(10).to_string(index=False))

# Save CSV
output_file = (
    OUTPUT_DIR / "state_transactions.csv"
)

df.to_csv(output_file, index=False)

print("\nCSV saved successfully!")
print(output_file)
