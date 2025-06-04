import os

from fastapi import FastAPI, File, UploadFile, HTTPException
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from oep.main import upload_with_local_path


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static/templates")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="main.html",
        status_code=200,
    )

@app.post("/upload/webform")
def upload_webform(files: list[UploadFile] = File(...)):
    for file in files:
        try:
            contents = file.file.read()
            with open(file.filename, 'wb') as f:
                f.write(contents)
        except Exception:
            raise HTTPException(status_code=500, detail='Something went wrong')
        finally:
            file.file.close()

@app.get("/upload/localdata/data")
def upload_localdata():
    data = os.path.abspath(os.path.join(os.getcwd(), "data"))
    print(data)

    response = upload_with_local_path(
        data_path=data,
        with_upload=False,
        topic="sandbox",
        token=os.getenv("OEP_API_TOKEN")
    )

    return response

@app.get("/upload/localdata/examples")
def upload_localdata_examples():
    data = os.path.abspath(os.path.join(os.getcwd(), "examples"))
    print(data)

    response = upload_with_local_path(
        data_path=data,
        with_upload=False,
        topic="sandbox",
        token=os.getenv("OEP_API_TOKEN")
    )

    return response