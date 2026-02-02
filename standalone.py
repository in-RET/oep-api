import json
import os
import sys

from pandas.core.common import fill_missing_names

from oep.main import OepUploader

TOKEN = os.getenv('OEP_API_TOKEN')
TOPIC = "sandbox"

print(f"OEP API Key: {TOKEN}")

data = [
    "data/demand/ghd_east.json",
    "data/demand/ghd_middle.json",
    "data/demand/ghd_north.json",
    "data/demand/ghd_swest.json",
    "data/demand/household_east.json",
    "data/demand/household_middle.json",
    "data/demand/household_north.json",
    "data/demand/household_swest.json",
    "data/demand/industry_east.json",
    "data/demand/industry_middle.json",
    "data/demand/industry_north.json",
    "data/demand/industry_swest.json",
    "data/demand/mobility.json"
]

for filename in data:
    print(f"Filename: {filename}")
    with open(filename, "r") as f:
        json_data = json.loads(f.read())

    table_name = json_data['name']
    #print(f"Table: {table_name}")
    if len(table_name) > 50:
        print(f"Table name too long: {table_name}", file=sys.stderr)
        break

    primary_key = json_data['resources'][0]['schema']['primaryKey'][0]
    #print(f"Primary Key: {primary_key}")

    delete_existing = True

    #print("=" * 60)
    #print(f"Uploading {table_name}...")
    #print(f"Table: {table_name}")
    try:
        uploader = OepUploader(token=TOKEN, topic=TOPIC)
        uploader.upload_complete(
            data_file=filename.replace(".json", ".csv"),
            table_name=table_name,
            metadata_file=filename,
            primary_key=primary_key,
            delete_existing=delete_existing
        )
        print("=" * 60)
    except Exception as e:
        print(f"\n Error: {str(e)}", file=sys.stderr)
