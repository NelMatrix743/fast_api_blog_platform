from typing import Annotated, Tuple
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.responses import Response, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from sqlalchemy import Result, or_, select
from sqlalchemy.orm import Session

from .schemas import PostCreate, PostResponse, UserCreate, UserResponse
from . import models
from .database import Base, engine, get_db
from .utils import generate_datetime
from .dummy_data import DUMMY_POSTS



Base.metadata.create_all(bind=engine)

SRC_DIR: Path = Path(__file__).resolve().parent

TEMPLATE_DIR: str = SRC_DIR / "templates"
STATIC_DIR: str = SRC_DIR / "static"
MEDIA_DIR: str = SRC_DIR / "media"

templates  = Jinja2Templates(directory=TEMPLATE_DIR)

app: FastAPI = FastAPI()

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")



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


@app.get("/posts/{post_id}", name="post", include_in_schema=False)
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
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found"
    )



# --- API INTERFACE ---
@app.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]) -> JSONResponse:
    result: Result[Tuple[models.User]] = db.execute(
        select(models.User)
        .where(
            or_(
                models.User.username == user.username,
                models.User.email == user.email
            )
        )
    )

    user_exist = result.scalars().first()

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exiss"
        )


@app.get("/api/posts", response_model=list[PostResponse])
def get_posts() -> JSONResponse:
    return DUMMY_POSTS


@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int) -> JSONResponse:
    for post in DUMMY_POSTS:  
        if post["id"] == post_id:
            return post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found"
    )


@app.post("/api/posts/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate) -> Response:
    post_id: int = max(p["id"] for p in DUMMY_POSTS) + 1 if DUMMY_POSTS else 1
    new_post: dict[str, any] = {
        "id" : post_id,
        "author" : post.author,
        "title" : post.title,
        "content" : post.content,
        "date_posted" : generate_datetime(),
    }

    DUMMY_POSTS.append(new_post)
    return new_post


# --- general exception handling ---
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(
    request: Request,
    exception: StarletteHTTPException) -> Response:
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check you request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail" : message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code" : exception.status_code,
            "title" : exception.status_code,
            "message" : message
        },
        status_code=exception.status_code
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(
    request: Request,
    exception: RequestValidationError
) -> Response:
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "detail" : exception.errors()
            }
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code" : status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title" : status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message" : "Invalid request. Please check your input and try again."
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
    )



# EOSC