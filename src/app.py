from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pathlib import Path



SRC_DIR = Path(__file__).resolve().parent

TEMPLATE_DIR: str = SRC_DIR / "templates"
STATIC_DIR: str = SRC_DIR / "static"

templates  = Jinja2Templates(directory=TEMPLATE_DIR)

app: FastAPI = FastAPI()

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# endpoints are defined here

@app.get('/')
def index(request: Request) -> Response:
    return templates.TemplateResponse(request, "index.html")


# EOSC