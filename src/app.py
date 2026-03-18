from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from pathlib import Path



app: FastAPI = FastAPI()

SRC_DIR = Path(__file__).resolve().parent
templates  = Jinja2Templates(directory=str(SRC_DIR / "templates"))

# endpoints are defined here

@app.get('/')
def index(request: Request) -> Response:
    return templates.TemplateResponse(request, "index.html")


# EOSC