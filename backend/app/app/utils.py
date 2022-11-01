import uuid
from enum import Enum

from fastapi import HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError

from app.core.config import settings


class Tag(str, Enum):
    login = "login"
    users = "users"
    posts = "posts"
    comments = "comments"
    profiles = "profiles"
    pictures = "pictures"


class Prefix(str, Enum):
    login = "/login"
    users = "/users"
    posts = "/posts"
    comments = "/comments"
    profiles = "/profiles"
    pictures = "/pictures"


class CustomHttpExceptions:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def save_picture(picture: UploadFile):
    try:
        image = Image.open(picture.file)
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid file type")
    if image.format not in settings.VALID_PICTURE_FORMATS:
        raise HTTPException(status_code=400, detail="Invalid picture format")
    fwidth, fheight = settings.PICTURE_OUTPUT_SIZE
    cwidth, cheight = image.size
    if cwidth < cwidth or cheight < fheight:
        raise HTTPException(status_code=400, detail="Image is too small")
    if cwidth > cheight:
        box = (int((cwidth - cheight) / 2), 0, int((cwidth + cheight) / 2), cheight)
        image = image.crop(box)
    elif cheight > cwidth:
        box = (0, int((cheight - cwidth) / 2), cwidth, int((cheight + cwidth) / 2))
        image = image.crop(box)
    cwidth, cheight = image.size
    if cwidth > fwidth or cheight > fheight:
        image = image.resize((fwidth, fheight))
    name = f"{uuid.uuid4().hex}.{settings.PICTURE_OUTPUT_FORMAT.lower()}"
    image.save(
        fp=f"{settings.PICTURE_OUTPUT_DIRECTORY}/{name}",
        format=settings.PICTURE_OUTPUT_FORMAT,
    )
    return name
