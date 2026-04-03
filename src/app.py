from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import Response, JSONResponse
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



# --- endpoints are defined here ---

# --- WEB INTERFACES ---
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


@app.get("/post/{post_id}", name="post", include_in_schema=False)
def get_post_page(request: Request, post_id: int) -> Response:
    for post in DUMMY_POSTS:
        if post["id"] == post_id:
            return templates.TemplateResponse(
                request,
                "post.html",
                {
                    "post" : post,
                    "title" : post["title"]
                }
            )
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found"
    )



# --- API INTERFACE ---
@app.get("/api/posts")
def get_posts() -> JSONResponse:
    return DUMMY_POSTS


@app.get("/api/posts/{post_id}")
def get_post(post_id: int) -> JSONResponse:
    for post in DUMMY_POSTS:
        if post["id"] == post_id:
            return post
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found"
    )


# EOSC