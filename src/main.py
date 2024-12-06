# install required packages with: pip install requests
# import required packages
import json
import os

import numpy as np
import pandas as pd

from random import randint
from oep_handler import OepHandler

topic = "sandbox"
table = f"tutorial_example_table_{randint(0, 100000)}"
token = os.environ.get("OEP_API_TOKEN") #% TODO: .env-File anlegen nicht vergessen!
print("Gewählter Token:", token)

# Create API-Handler-Object
OepApi = OepHandler(f"https://openenergyplatform.org/api/v0/schema/{topic}/tables/{table}/", token)

data_path = os.path.abspath(os.path.join("data"))
print("Datenpfad:", data_path)

for root, dirs, files in os.walk(data_path, topdown=True):
    pass # TODO for later

raw_csv = pd.read_csv(
    filepath_or_buffer=os.path.join(data_path, "scalars", "parameter", "parameter_onshore_wind_power_plant_inret.csv"),
    index_col=0,
    sep=';',
    decimal='.',
    encoding = 'unicode_escape'
)

raw_data = raw_csv.loc["data", :] # Pandas ist geil
raw_meta = raw_csv.loc[["type", "unit", "isAbout", "description", "primary_key", "valueReference"], :]

table_schema_data = []

for key in raw_data.keys():
    table_schema_data.append({
        "name": key,
        "data_type": raw_meta.loc["type", key],
        "primary_key": raw_meta.loc["primary_key", key] if raw_meta.loc["primary_key", key] is not np.nan else None,
    })


print(json.dumps(table_schema_data))

table_schema = {
    "columns": table_schema_data # TODO Einlesen aus dem Ordner "data"
}
print(OepApi.create_table(table_schema))
print(
    f"you can see the data on the platform here: https://openenergyplatform.org/dataedit/view/{topic}/{table}"
)
# table_data = None # TODO Einlesen der Tabellendaten aus dem Ordner Data
