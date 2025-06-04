import json

import numpy as np
import requests as req


def create_tableschema(meta) -> dict[str, list[dict]]:
    table_schema_data = []

    for key in meta.keys():
        table_schema_data.append({
            "name": key,
            "data_type": meta.loc["data_type", key],
            "primary_key": meta.loc["primary_key", key] if meta.loc["primary_key", key] is not np.nan else None
        })

    return_schema = {"columns": table_schema_data}

    return return_schema

def create_tabledata_params(data) -> list[dict]:
    return json.loads(data.to_json(orient="records"))

def create_tabledata_sequences(data, meta) -> list[dict]:
    #print(meta.loc["description"])
    data_dict = []

    for row in data.index:
        data_row = []
        for index in data.keys():
            data_row.append(data.loc[row, index])
            data_dict.append({
                index: list(data[index])
            })

    return data_dict

def create_metadata(data) -> (list[dict], list, list):
    tmp_json = json.loads(data.to_json(orient="columns"))

    meta_data = []

    for index in tmp_json:
        data_dict = tmp_json[index]
        data_dict["name"] = index

        if not bool(data_dict["unit"]):
            data_dict["unit"] = ""

        if "primary_key" in data_dict:
            if bool(data_dict["primary_key"]):
                data_dict["primary_key"] = bool(tmp_json[index]["primary_key"])
            else:
                del(data_dict["primary_key"])
        else:
            data_dict["primary_key"] = "id"

        data_dict["nullable"] = True
        meta_data.append(data_dict)

    return meta_data

def translate_response(func: str, response: req.Response):
    if not response.ok:
        raise Exception(response.text)
    else:
        return f'%s: Request successful.' % func
