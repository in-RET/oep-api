import requests as req

from .auxillary import translate_response

class OepHandler:
    auth_header = None
    api_url = None
    context = {
        "contact": "Hochschule Nordhausen - Institut für regenerative Energietechnik",
        "homepage": "https://hs-nordhausen.de",
        "documentation": "https://hs-nordhausen.de",
        "sourceCode": "https://github.com/in-RET"
    }

    def __init__(self, api_url, token):
        self.api_url = api_url
        self.auth_header = {"Authorization": "Token %s" % token}

        #print("AUTH_HEADER", self.auth_header)
        #print("API_URL:",  self.api_url)


    def create_table(self, table_schema: dict[str, list[dict]]) -> str:
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

    def upload_metadata(self, data) -> str:
        return translate_response(
            func="upload_metadata",
            response=req.post(self.api_url + "meta/", json=data, headers=self.auth_header)
        )

