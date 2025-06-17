import os
from random import randint

import pandas as pd

from .auxillary import *
from .handler import OepHandler


def upload_with_local_path(data_path: str, with_upload: bool = False, topic: str = "sandbox"):
    messages = [f"Datenpfad: {data_path}"]

    for root, dirs, files in os.walk(data_path, topdown=True):
        for file in files:
            if file.startswith("parameter_") and file.endswith(".csv"):
                messages.append(f"{file}")
                table = f"%s_{randint(0, 100)}" % file.replace(".csv", "")
                raw_csv = pd.read_csv(
                    filepath_or_buffer=os.path.join(data_path, "parameter", file),
                    index_col=0,
                    sep=';',
                    decimal='.',
                    encoding = 'unicode_escape'
                )

                # Create API-Handler-Object
                OepApi = OepHandler(
                    table_name=table,
                    topic=topic,
                )

                raw_data = raw_csv.loc["data", :] # Pandas ist geil
                raw_meta = raw_csv.loc[["data_type", "type", "unit", "description", "primary_key"], :]

                ########################################################################################################################
                #   Create Table Schema
                ########################################################################################################################
                table_schema = create_tableschema(raw_meta)

                ########################################################################################################################
                #   Upload Table Schema
                ########################################################################################################################
                if with_upload:
                    response = OepApi.create_table(table_schema)
                    messages.append(response)

                ########################################################################################################################
                #   Create Table Data
                ########################################################################################################################
                table_data = create_tabledata_params(raw_data)

                ########################################################################################################################
                #   Upload Table Data
                ########################################################################################################################
                if with_upload:
                    response = OepApi.upload_data(table_data)
                    messages.append(response)

                ########################################################################################################################
                #   Create Meta Data
                ########################################################################################################################
                meta_fields = create_metadata(raw_meta)

                with open(os.path.join(data_path, "parameter", file.replace(".csv", ".json"))) as f:
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
                if with_upload:
                    response = OepApi.upload_metadata(meta_data)
                    messages.append(response)

                messages.append(f"https://openenergyplatform.org/dataedit/view/{topic}/{table}")
            elif file.startswith("sequences_") and file.endswith(".csv"):
                messages.append(file)
                table = f"%s_{randint(0, 100)}" % file.replace(".csv", "").replace("_for", "").replace("_selected","").replace("_in", "").replace("_thuringia", "_th").replace("sequences", "seq")
                raw_csv = pd.read_csv(
                    filepath_or_buffer=os.path.join(data_path, file),
                    index_col=0,
                    sep=';',
                    decimal='.',
                    encoding = 'unicode_escape'
                )

                # Create API-Handler-Object
                OepApi = OepHandler(
                    table_name=table,
                    topic=topic,
                )

                raw_data = raw_csv.loc["data", :] # Pandas ist geil
                raw_data.index = np.linspace(0,8759, 8760, dtype=int)
                raw_meta = raw_csv.loc[["data_type", "type", "unit", "primary_key", "description"], :]

                ########################################################################################################################
                #   Create Table Schema
                ########################################################################################################################
                table_schema = create_tableschema(raw_meta)
                table_schema["columns"].append({
                    'name': 'id',
                    'data_type': 'int',
                    'primary_key': True
                })

                ########################################################################################################################
                #   Upload Table Schema
                ########################################################################################################################
                if with_upload:
                    response = OepApi.create_table(table_schema)
                    messages.append(response)
                else:
                    with open("debug_schema.json", "wt") as f:
                        json.dump(table_schema, f, ensure_ascii=False, indent=2)

                ########################################################################################################################
                #   Create Table Data
                ########################################################################################################################
                table_data = json.loads(raw_data.to_json(orient="records")) #create_tabledata_sequences(raw_data, raw_meta)

                ####################################################################r####################################################
                #   Upload Table Data
                ########################################################################################################################
                if with_upload:
                    response = OepApi.upload_data(table_data)
                    messages.append(response)
                else:
                    with open("debug_data.json", "wt") as f:
                        json.dump(table_data, f, ensure_ascii=False, indent=2)

                ########################################################################################################################
                #   Create Meta Data
                ########################################################################################################################
                meta_fields = create_metadata(raw_meta)

                with open(os.path.join(data_path, file.replace(".csv", ".json"))) as f:
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


                ########################################################################################################################
                #   Upload Meta Data
                ########################################################################################################################
                if with_upload:
                    response = OepApi.upload_metadata(meta_data)
                    messages.append(response)
                else:
                    with open('debug_meta.json', 'wt') as f:
                        json.dump(meta_data, f, ensure_ascii=False, indent=2)

                messages.append(f"https://openenergyplatform.org/dataedit/view/{topic}/{table}")
            else:
                messages.append(f"Nicht bearbeitete Datei: {file}")

    return messages







