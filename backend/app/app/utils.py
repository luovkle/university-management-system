import uuid
import shutil
import pathlib
from enum import Enum

from fastapi import HTTPException, status, UploadFile

from app.core.config import settings


class Tag(str, Enum):
    login = "login"
    users = "users"
    posts = "posts"
    comments = "comments"
    profiles = "profiles"
    pictures = "pictures"
    tasks = "tasks"


class Prefix(str, Enum):
    login = "/login"
    users = "/users"
    posts = "/posts"
    comments = "/comments"
    profiles = "/profiles"
    pictures = "/pictures"
    tasks = "/tasks"


class CustomHttpExceptions:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def save_temp_picture(picture: UploadFile):
    temp_file = uuid.uuid4().hex
    temp_path = f"{settings.PICTURE_OUTPUT_DIRECTORY}/{temp_file}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(picture.file, buffer)
    return temp_path


def delete_temp_picture(picture: str):
    path = pathlib.Path(picture)
    if path.exists():
        path.unlink()
