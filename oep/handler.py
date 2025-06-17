import os

from oep_client.oep_client import OepClient


class OepHandler():
    client: OepClient
    table_name: str
    token: str = os.getenv("OEP_API_TOKEN")
    topic: str = "sandbox"
    context: dict = {
        "contact": "Hochschule Nordhausen - Institut für regenerative Energietechnik",
        "homepage": "https://hs-nordhausen.de",
        "documentation": "https://hs-nordhausen.de",
        "sourceCode": "https://github.com/in-RET"
    }

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, table_name: str, topic: str = "sandbox"):
        self.table_name = table_name
        self.topic = topic
        self.client = OepClient(
            token=self.token,
            default_schema=self.topic
        )

    def create_table(self, table_schema: dict[str, list[dict]]) -> str:
        return self.client.create_table(
            table=self.table_name,
            definition=table_schema
        )

    def delete_table(self) -> str:
        return self.client.drop_table(
            table=self.table_name
        )

    def upload_data(self, data: list[dict[str, str]]) -> str:
        return self.client.insert_into_table(
            table=self.table_name,
            data=data
        )

    def upload_metadata(self, data) -> str:
        return self.client.set_metadata(
            table=self.table_name,
            metadata=data
        )
