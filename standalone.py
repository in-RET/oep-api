import os
import sys

import numpy as np

from oep.main import OepUploader

TOKEN = os.getenv('OEP_API_TOKEN')
TOPIC = "sandbox"

print(f"OEP API Key: {TOKEN}")

data = [
    ("data/parameter_photovoltaik_openfield.json", "data/parameter_photovoltaik_openfield.csv"),
    ("data/parameter_photovoltaik_rooftop.json", "data/parameter_photovoltaik_rooftop.csv")
]

for meta_file, data_file in data:
    table_name = meta_file.replace('.json', '').replace('data/', '') + "_" + str(np.random.randint(1000))
    primary_key = None
    delete_existing = True

    print("============================================================")
    print(f"Uploading {table_name}...")
    print(f"Table: {table_name}")
    try:
        uploader = OepUploader(token=TOKEN, topic=TOPIC)
        uploader.upload_complete(
            data_file=data_file,
            table_name=table_name,
            metadata_file=meta_file,
            primary_key=primary_key,
            delete_existing=delete_existing
        )
    except Exception as e:
        print(f"\n Error: {str(e)}", file=sys.stderr)
