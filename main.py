import os
import json
import pandas as pd

from random import randint
from src.oep_handler import OepHandler, create_tabledata, create_tableschema, create_metadata

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
    encoding="unicode_escape"
)


for root, dirs, files in os.walk(data_path, topdown=True):
    pass # TODO for later

raw_file_name = "parameter_onshore_wind_power_plant_inret.csv"
table = f"%s_{randint(0, 100000)}" % raw_file_name.replace(".csv", "")
raw_csv = pd.read_csv(
    filepath_or_buffer=os.path.join(data_path, "scalars", "parameter", raw_file_name),
    index_col=0,
    sep=';',
    decimal='.',
    encoding = 'unicode_escape'
)

# Create API-Handler-Object
OepApi = OepHandler(f"https://openenergyplatform.org/api/v0/schema/{topic}/tables/{table}/", token)

raw_data = raw_csv.loc["data", :] # Pandas ist geil
raw_meta = raw_csv.loc[["type", "unit", "isAbout", "description", "primary_key", "valueReference"], :]

table_schema = create_tableschema(raw_data, raw_meta)
response = OepApi.create_table(table_schema)
#print(response)

table_data = create_tabledata(raw_data)
#response = OepApi.upload_data(table_data)
#print(response)


meta_data = json.loads(general_meta.to_json(orient="columns"))["Unnamed: 1"]
meta_data["id"] = raw_file_name.replace(".csv", "")
meta_data["resources"] = {
    "name": raw_file_name.replace(".csv", ""),
    "schema": {
        "fields": create_metadata(raw_meta)
    }
}


response = OepApi.upload_metadata(meta_data)
print(response)

print(f"https://openenergyplatform.org/dataedit/view/{topic}/{table}")









