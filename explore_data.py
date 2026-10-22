
from pathlib import Path
import json

# Locate the official PhonePe Pulse dataset
project_folder = Path(__file__).resolve().parent

data_folder = (
    project_folder
    / "pulse-main"
    / "data"
    / "aggregated"
    / "transaction"
    / "country"
    / "india"
)

# Find available yearly folders
if not data_folder.exists():
    print("Dataset folder not found!")
    print("Expected location:", data_folder)
else:
    print("Dataset found successfully!")

    years = sorted(
        folder.name
        for folder in data_folder.iterdir()
        if folder.is_dir()
    )

    print("Available years:", years)

    # Read a sample JSON file
    json_files = sorted(data_folder.rglob("*.json"))

    print("Total JSON files:", len(json_files))

    if json_files:
        with open(
            json_files[0],
            "r",
            encoding="utf-8"
        ) as file:
            sample = json.load(file)

        print("\nSample JSON structure:")
        print(json.dumps(sample, indent=2)[:2000])


# ==========================================
# STEP 4: INSPECT TRANSACTION DATA STRUCTURE
# ==========================================

sample_file = (
    data_folder / "2024" / "1.json"
)

if sample_file.exists():

    with open(
        sample_file, "r", encoding="utf-8"
    ) as file:
        data = json.load(file)

    print("\nTOP LEVEL KEYS:")
    print(list(data.keys()))

    print("\nDATA KEYS:")
    print(list(data.get("data", {}).keys()))

    print("\nFIRST TRANSACTION CATEGORY:")

    categories = (
        data.get("data", {})
        .get("transactionData") or []
    )

    if categories:
        print(json.dumps(
            categories[0],
            indent=2
        ))
    else:
        print("No transaction categories found.")

else:
    print("Sample file not found:", sample_file)


# ==========================================
# STEP 5: EXPLORE AVAILABLE DATASETS
# ==========================================

from pathlib import Path

pulse_data = (
    Path(__file__).resolve().parent
    / "pulse-main"
    / "data"
)

print("\nAVAILABLE DATASET DIRECTORIES:\n")

for category in sorted(pulse_data.iterdir()):

    if category.is_dir():

        print(f"\n{category.name.upper()}")

        for subfolder in sorted(category.iterdir()):

            if subfolder.is_dir():
                print("  -", subfolder.name)

print("\nSAMPLE JSON STRUCTURES:\n")

for dataset_type in ["aggregated", "map", "top"]:

    dataset_path = pulse_data / dataset_type

    if not dataset_path.exists():
        continue

    for subfolder in sorted(dataset_path.iterdir()):

        if not subfolder.is_dir():
            continue

        files = sorted(subfolder.rglob("*.json"))

        if not files:
            continue

        with open(
            files[0], "r", encoding="utf-8"
        ) as file:
            sample = json.load(file)

        print(
            dataset_type,
            "/",
            subfolder.name,
            "=>",
            list(sample.get("data", {}).keys())
        )


# ==========================================
# STEP 6: FIND AND INSPECT MAP TRANSACTIONS
# ==========================================

map_transaction_path = (
    pulse_data / "map" / "transaction"
)

# Find JSON files automatically
json_files = sorted(
    map_transaction_path.rglob("*.json")
)

print("\nMAP TRANSACTION FILES FOUND:",
      len(json_files))

if json_files:

    # Display the first 5 file paths
    print("\nSAMPLE FILE PATHS:")

    for file_path in json_files[:5]:
        print(file_path.relative_to(pulse_data))

    # Read the first JSON file
    sample_file = json_files[0]

    with open(
        sample_file, "r", encoding="utf-8"
    ) as file:
        data = json.load(file)

    print("\nDATA KEYS:")
    print(list(data.get("data", {}).keys()))

    locations = (
        data.get("data", {})
        .get("hoverDataList") or []
    )

    print("\nTOTAL LOCATIONS:", len(locations))

    if locations:
        print("\nFIRST LOCATION RECORD:")
        print(json.dumps(locations[0], indent=2))

else:
    print("No JSON files found.")
