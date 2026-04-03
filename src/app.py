from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pathlib import Path

from .dummy_data import DUMMY_POSTS



SRC_DIR = Path(__file__).resolve().parent

TEMPLATE_DIR: str = SRC_DIR / "templates"
STATIC_DIR: str = SRC_DIR / "static"

templates  = Jinja2Templates(directory=TEMPLATE_DIR)

app: FastAPI = FastAPI()

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# endpoints are defined here

@app.get('/', name="home", include_in_schema=False)
def index(request: Request) -> Response:
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "title" : "Home",
            "posts" : DUMMY_POSTS
        }
    )


@app.get("/api/posts")
def get_posts():
    return DUMMY_POSTS


# EOSC