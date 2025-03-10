import os
import json

import numpy as np
import pandas as pd

from random import randint

from numpy.ma.core import transpose

from src.oep_handler import OepHandler, create_tabledata_params, create_tabledata_sequences, create_tableschema, create_metadata

WITH_UPLOAD = True

topic = "sandbox"
token = os.environ.get("OEP_API_TOKEN") #% TODO: .env-File anlegen nicht vergessen!
print("Gewählter Token:", token)

data_path = os.path.abspath(os.path.join("data"))
print("Datenpfad:", data_path)

general_meta = pd.read_csv(
    filepath_or_buffer=os.path.join(data_path, "meta_data_general.csv"),
    index_col=0,
    sep=";",
    decimal=".",
)

for root, dirs, files in os.walk(data_path, topdown=True):
    for file in files:
        if False: #file.startswith("parameter_"):
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
            table_schema = create_tableschema(raw_data, raw_meta)

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

            meta_data = general_meta.to_dict()["value"]
            meta_data["id"] = table
            meta_data["name"] = table.replace("_", " ")
            meta_data["keywords"] = []
            meta_data["subject"] = ["Debugging purposes"],
            meta_data["languages"] = ["EN"]
            meta_data["licenses"] = [
                {
                    "name": "CC-BY-4.0",
                    "path": "https://spdx.github.io/license-list-data/CC-BY-4.0.html",
                    "title": "Creative Commons Attribution 4.0 International"
                }
            ]
            meta_data["context"] = OepApi.context
            meta_data["resources"] = [{
                "name": table,
                "schema": {
                    "fields": meta_fields
                }
            }]

            with open('meta_debug.json', 'w', encoding='utf-8') as f:
                json.dump(meta_data, f, ensure_ascii=False, indent=2)

            ########################################################################################################################
            #   Upload Meta Data
            ########################################################################################################################
            if WITH_UPLOAD:
                response = OepApi.upload_metadata(meta_data)
                print(response)

            print(f"https://openenergyplatform.org/dataedit/view/{topic}/{table}")
        elif file.startswith("sequences_"):
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
            table_schema = create_tableschema(raw_meta)

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

            meta_data = general_meta.to_dict()["value"]
            meta_data["id"] = table
            meta_data["name"] = table.replace("_", " ")
            meta_data["keywords"] = []
            meta_data["subject"] = ["Debugging purposes"],
            meta_data["languages"] = ["EN"]
            meta_data["licenses"] = [
                {
                    "name": "CC-BY-4.0",
                    "path": "https://spdx.github.io/license-list-data/CC-BY-4.0.html",
                    "title": "Creative Commons Attribution 4.0 International"
                }
            ]
            meta_data["context"] = OepApi.context
            meta_data["resources"] = [{
                "name": table,
                "schema": {
                    "fields": meta_fields
                }
            }]

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








