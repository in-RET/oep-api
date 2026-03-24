import json
import os
import sys

import pandas as pd

from oep.main import OepUploader

TOKEN = os.getenv('OEP_API_TOKEN')
TOPIC = "sandbox"
AUTOMATIC_SCAN = True

print(f"OEP API Key: {TOKEN}")

upload_list = []

if AUTOMATIC_SCAN:
    for root, dir, files in os.walk("data"):
        for filename in files:
            if filename.endswith(".json"):
                upload_list.append(os.path.join(root, filename))
else:
    upload_list.append("data/pricetimeseries/biomass.json")
    upload_list.append("data/pricetimeseries/brown_coal.json")
    upload_list.append("data/pricetimeseries/co2.json")
    upload_list.append("data/pricetimeseries/electricity.json")
    upload_list.append("data/pricetimeseries/gas.json")
    upload_list.append("data/pricetimeseries/hard_coal.json")
    upload_list.append("data/pricetimeseries/hydrogen.json")
    upload_list.append("data/pricetimeseries/oil.json")
    upload_list.append("data/pricetimeseries/ptl.json")
    upload_list.append("data/parameter/power_to_liquid_system.json")
    upload_list.append("data/parameter/photovoltaic_openfield.json")
    upload_list.append("data/feed_in_profile/ambient_temperature_east.json")
    upload_list.append("data/feed_in_profile/ambient_temperature_north.json")
    upload_list.append("data/feed_in_profile/ambient_temperature_middle.json")
    upload_list.append("data/feed_in_profile/ambient_temperature_swest.json")
    upload_list.append("data/feed_in_profile/hydropower.json")
    upload_list.append("data/demand_profile/mobility.json")

print(f"Uploading {len(upload_list)} files...")
#print(upload_list)

table_names = []

for filename in upload_list:
    print(f"Filename: {filename}")
    with open(filename, "r") as f:
        json_data = json.loads(f.read())

    table_name = json_data['name']

    table_names.append(table_name)

print(f"Table names: {table_names}")

pd.Series(table_names).to_csv(path_or_buf="table_names.csv", index=False, header=False)

    #print(f"Table: {table_name}")



    # if len(table_name) > 50:
    #     print(f"Table name too long: {table_name}", file=sys.stderr)
    #     print(f"Length: {len(table_name)}", file=sys.stderr)
    # else:
    #     primary_key = json_data['resources'][0]['schema']['primaryKey'][0]
    #     #print(f"Primary Key: {primary_key}")
    #
    #     delete_existing = True
    #
    #     #print("=" * 60)
    #     #print(f"Uploading {table_name}...")
    #     #print(f"Table: {table_name}")
    #     try:
    #         uploader = OepUploader(token=TOKEN, topic=TOPIC)
    #         # uploader.delete_table(table_name)
    #         uploader.upload_complete(
    #             data_file=filename.replace(".json", ".csv"),
    #             table_name=table_name,
    #             metadata_file=filename,
    #             primary_key=primary_key,
    #             delete_existing=delete_existing
    #         )
    #         print("=" * 60)
    #     except Exception as e:
    #         print(f"\n Error: {str(e)}", file=sys.stderr)
