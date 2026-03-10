import json
import os
import sys

from oep.main import OepUploader

TOKEN = os.getenv('OEP_API_TOKEN')
TOPIC = "sandbox"

print(f"OEP API Key: {TOKEN}")

upload_list = []

for root, dir, files in os.walk("data"):
    for filename in files:
        if filename.endswith(".json"):
            upload_list.append(os.path.join(root, filename))

print(f"Uploading {len(upload_list)} files...")
print(upload_list)

for filename in upload_list:
    print(f"Filename: {filename}")
    with open(filename, "r") as f:
        json_data = json.loads(f.read())

    table_name = json_data['name']
    #print(f"Table: {table_name}")
    if len(table_name) > 50:
        print(f"Table name too long: {table_name}", file=sys.stderr)
        print(f"Length: {len(table_name)}", file=sys.stderr)
    else:
        primary_key = json_data['resources'][0]['schema']['primaryKey'][0]
        #print(f"Primary Key: {primary_key}")

        delete_existing = True

        #print("=" * 60)
        #print(f"Uploading {table_name}...")
        #print(f"Table: {table_name}")
        try:
            uploader = OepUploader(token=TOKEN, topic=TOPIC)
            uploader.delete_table(table_name)
            # uploader.upload_complete(
            #     data_file=filename.replace(".json", ".csv"),
            #     table_name=table_name,
            #     metadata_file=filename,
            #     primary_key=primary_key,
            #     delete_existing=delete_existing
            # )
            print("=" * 60)
        except Exception as e:
            print(f"\n Error: {str(e)}", file=sys.stderr)
