import requests as req

class OepHandler:
    auth_header = None
    api_url = None

    def __init__(self, api_url, token):
        self.api_url = api_url
        self.auth_headers = {"Authorization": "Token %s" % token}

    def create_table(self, table_schema: dict[str, list[dict[str, None]]]) -> str:
        res = req.put(self.api_url, json={"query": table_schema}, headers=self.auth_header)
        return res.text

    def delete_table(self) -> str:
        res = req.delete(self.api_url, headers=self.auth_header)

        return res.text

    def upload_data(self, data: list[dict[str, str]]) -> str:
        res = req.post(self.api_url + "rows/new", json={"query": data}, headers=self.auth_header)

        return res.text

    def upload_metadata(self, data: list[dict[str, str]]) -> str:
        res = req.post(self.api_url + "meta/", json=data, headers=self.auth_header)

        return res.text

