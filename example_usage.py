"""
Example script demonstrating how to use the OEP Uploader programmatically
"""

from oep.uploader import OepUploader
import pandas as pd

# Example 1: Create test data
print("Example 1: Creating test data")
print("="*60)

test_data = pd.DataFrame({
    'year': [2025, 2030, 2035, 2040, 2045, 2050],
    'investment_costs': [600000, 550000, 505000, 463000, 390000, 309000],
    'operating_costs': [2, 2, 2, 2, 2, 2],
    'lifetime': [25, 25, 25, 25, 25, 25],
    'interest_rate': [5, 5, 5, 5, 5, 5]
})

print(test_data)
print()

# Example 2: Read existing data
print("Example 2: Reading existing data")
print("="*60)

# Note: You need to set OEP_API_TOKEN environment variable to actually upload
# export OEP_API_TOKEN="your-token-here"

try:
    uploader = OepUploader(topic="sandbox")

    # Read data from file
    df = uploader.read_data("data/parameter_photovoltaik_openfield.csv")
    print(f"Data loaded: {len(df)} rows, {len(df.columns)} columns")
    print(f"Columns: {', '.join(df.columns.tolist())}")
    print()
    print(df.head())
    print()

    # Create table schema
    schema = uploader.create_table_schema(df, primary_key="year")
    print("Generated schema:")
    import json
    print(json.dumps(schema, indent=2))
    print()

    # Convert to records (format for OEP upload)
    records = uploader.dataframe_to_records(df)
    print(f"Converted to {len(records)} records for upload")
    print("First record:")
    print(json.dumps(records[0], indent=2))

except ValueError as e:
    print(f"Note: {e}")
    print("Set the OEP_API_TOKEN environment variable to use the uploader.")
except FileNotFoundError as e:
    print(f"File not found: {e}")
    print("Make sure you're running this from the project root directory.")

print()
print("="*60)
print("To actually upload data, use:")
print("python oep/uploader.py --data data/parameter_photovoltaik_openfield.csv --table my_test_table")

