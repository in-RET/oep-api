import os

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from oep.main import upload_with_local_path

app = FastAPI()


origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static/templates")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="main.html",
        status_code=200,
        context={"datapath": os.path.abspath(os.path.join(os.getcwd(), "examples", "sequences"))},
    )

@app.post("/upload/localdata")
async def upload_localdata(datapath: str = Form(), with_upload: bool = Form(), topic:str = Form("sandbox")) -> JSONResponse:
    msg = upload_with_local_path(
        data_path=datapath,
        with_upload=with_upload,
        topic=topic,
        token=os.getenv("OEP_API_TOKEN")
    )

    return JSONResponse(
        content=msg,
        status_code=200,
    )

@app.get("/upload/localdata/examples")
async def upload_localdata_examples():
    data = os.path.abspath(os.path.join(os.getcwd(), "examples"))
    print(data)

    response = upload_with_local_path(
        data_path=data,
        with_upload=False,
        topic="sandbox",
        token=os.getenv("OEP_API_TOKEN")
    )

    return response