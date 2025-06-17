import os

from oep.main import upload_with_local_path

print(os.getenv("OEP_API_TOKEN"))
datapath = os.path.abspath(os.path.join(os.getcwd(), "examples", "scalars"))
print(datapath)

messages = upload_with_local_path(
    data_path=datapath,
    with_upload=True,
    topic="model_draft"
)

print(messages)