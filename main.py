import json
import os
from random import randint

import numpy as np
import pandas as pd

from src.oep_handler import OepHandler, create_tabledata_params, create_tabledata_sequences, create_tableschema, \
    create_metadata

WITH_UPLOAD = True

topic = "sandbox" #"model_draft"
token = os.environ.get("OEP_API_TOKEN") #% TODO: .env-File anlegen nicht vergessen!
print("Gewählter Token:", token)

data_path = os.path.abspath(os.path.join("data"))
print("Datenpfad:", data_path)

for root, dirs, files in os.walk(data_path, topdown=True):
    for file in files:
        if file.startswith("parameter_") and file.endswith(".csv"):
            print(file)
            table = f"%s_{randint(0, 100000)}" % file.replace(".csv", "")
            raw_csv = pd.read_csv(
                filepath_or_buffer=os.path.join(data_path, "scalars", "parameter", file),
                index_col=0,
                sep=';',
                decimal='.',
                encoding = 'unicode_escape'
            )

            # Create API-Handler-Object
            OepApi = OepHandler(f"https://openenergyplatform.org/api/v0/schema/{topic}/tables/{table}/", token)

            raw_data = raw_csv.loc["data", :] # Pandas ist geil
            raw_meta = raw_csv.loc[["data_type", "type", "unit", "description", "primary_key"], :]

            ########################################################################################################################
            #   Create Table Schema
            ########################################################################################################################
            table_schema = create_tableschema(raw_meta, "scalars")

            ########################################################################################################################
            #   Upload Table Schema
            ########################################################################################################################
            if WITH_UPLOAD:
                response = OepApi.create_table(table_schema)
                print(response)

            ########################################################################################################################
            #   Create Table Data
            ########################################################################################################################
            table_data = create_tabledata_params(raw_data)

            ########################################################################################################################
            #   Upload Table Data
            ########################################################################################################################
            if WITH_UPLOAD:
                response = OepApi.upload_data(table_data)
                print(response)

            ########################################################################################################################
            #   Create Meta Data
            ########################################################################################################################
            meta_fields = create_metadata(raw_meta)

            with open(os.path.join(data_path, "scalars", "parameter", file.replace(".csv", ".json"))) as f:
                meta_data = json.load(f)

            meta_data["name"] = table.replace("_", " ")
            meta_data["title"] = table.replace("_", " ")
            meta_data["resources"][0].update({
                "name": table,
                "schema": {
                    "fields": meta_fields,
                    "primaryKey": ["id"]
                }
            })

            # with open('meta_debug.json', 'w', encoding='utf-8') as f:
            #      json.dump(meta_data, f, ensure_ascii=False, indent=2)

            ########################################################################################################################
            #   Upload Meta Data
            ########################################################################################################################
            if WITH_UPLOAD:
                response = OepApi.upload_metadata(meta_data)
                print(response)

            print(f"https://openenergyplatform.org/dataedit/view/{topic}/{table}")
        elif file.startswith("sequences_") and file.endswith(".csv"):
            print(file)
            table = f"%s_{randint(0, 100000)}" % file.replace(".csv", "")
            raw_csv = pd.read_csv(
                filepath_or_buffer=os.path.join(data_path, "sequences", file),
                index_col=0,
                sep=';',
                decimal='.',
                encoding = 'unicode_escape'
            )

            # Create API-Handler-Object
            OepApi = OepHandler(f"https://openenergyplatform.org/api/v0/schema/{topic}/tables/{table}/", token)

            raw_data = raw_csv.loc["data", :] # Pandas ist geil
            raw_data.index = np.linspace(0,8759, 8760, dtype=int)
            raw_meta = raw_csv.loc[["data_type", "type", "unit", "description"], :]

            ########################################################################################################################
            #   Create Table Schema
            ########################################################################################################################
            table_schema = create_tableschema(raw_meta, "sequences")

            ########################################################################################################################
            #   Upload Table Schema
            ########################################################################################################################
            if WITH_UPLOAD:
                response = OepApi.create_table(table_schema)
                print(response)

            ########################################################################################################################
            #   Create Table Data
            ########################################################################################################################
            table_data = create_tabledata_sequences(raw_data, raw_meta)

            ####################################################################r####################################################
            #   Upload Table Data
            ########################################################################################################################
            if WITH_UPLOAD:
                response = OepApi.upload_data(table_data)
                print(response)

            ########################################################################################################################
            #   Create Meta Data
            ########################################################################################################################
            meta_fields = create_metadata(raw_meta)

            with open(os.path.join(data_path, "sequences", file.replace(".csv", ".json"))) as f:
                meta_data = json.load(f)

            meta_data["name"] = table.replace("_", " ")
            meta_data["title"] = table.replace("_", " ")
            meta_data["resources"][0].update({
                "name": table,
                "schema": {
                    "fields": meta_fields,
                    "primaryKey": ["id"]
                }
            })

            # with open('meta_debug.json', 'w', encoding='utf-8') as f:
            #     json.dump(meta_data, f, ensure_ascii=False, indent=2)

            ########################################################################################################################
            #   Upload Meta Data
            ########################################################################################################################
            if WITH_UPLOAD:
                response = OepApi.upload_metadata(meta_data)
                print(response)

            print(f"https://openenergyplatform.org/dataedit/view/{topic}/{table}")
        else:
            print("Nicht bearbeitete Datei:", file)








