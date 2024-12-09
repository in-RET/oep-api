import requests as req
import numpy as np
import json

def create_tableschema(data, meta) -> dict:
    table_schema_data = []

    for key in data.keys():
        table_schema_data.append({
            "name": key,
            "data_type": meta.loc["type", key],
            "primary_key": meta.loc["primary_key", key] if meta.loc["primary_key", key] is not np.nan else None
        })

    return {"columns": table_schema_data}

def create_tabledata(data) -> list[dict]:
    # print(data.to_json(orient="records"))
    return data.to_json(orient="records")

def create_metadata(data) -> list[dict]:
    tmp_json = json.loads(data.to_json(orient="columns"))

    meta_data = []

    for index in tmp_json:
        data_dict = tmp_json[index]
        data_dict["name"] = index

        meta_data.append(data_dict)

    return meta_data

def translate_response(func: str, response: req.Response):
    if not response.ok:
        return f'%s: %s' % (func, response.text)
    else:
        return f'%s: Request successful.' % func


class OepHandler:
    auth_header = None
    api_url = None

    def __init__(self, api_url, token):
        self.api_url = api_url
        self.auth_header = {"Authorization": "Token %s" % token}

        print("AUTH_HEADER", self.auth_header)
        print("API_URL:",  self.api_url)

    def create_table(self, table_schema: dict[str, list[dict[str, None]]]) -> str:
        return translate_response(
            func="create_table",
            response=req.put(self.api_url, json={"query": table_schema}, headers=self.auth_header)
        )

    def delete_table(self) -> str:
        return translate_response(
            func="delete_table",
            response=req.delete(self.api_url, headers=self.auth_header)
        )

    def upload_data(self, data: list[dict[str, str]]) -> str:
        return translate_response(
            func="upload_data",
            response=req.post(self.api_url + "rows/new", json={"query": data}, headers=self.auth_header)
        )

    def upload_metadata(self, data: list[dict[str, str]]) -> str:
        return translate_response(
            func="upload_metadata",
            response=req.post(self.api_url + "meta/", json=data, headers=self.auth_header)
        )

