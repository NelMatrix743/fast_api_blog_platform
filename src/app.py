from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from pathlib import Path



app: FastAPI = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates  = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# endpoints are defined here

@app.get('/')
def index(request: Request) -> Response:
    context: dict[str, str] = {
        "name" : "Nelmatrix"
    }
    return templates.TemplateResponse(request, "index.html", context)


# EOSC