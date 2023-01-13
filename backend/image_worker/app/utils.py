import pathlib
import shutil
import uuid
from enum import Enum

from PIL import Image, UnidentifiedImageError
from fastapi import UploadFile

from app.core.config import settings


class Tag(str, Enum):
    pictures = "pictures"
    tasks = "tasks"


class Prefix(str, Enum):
    pictures = "/pictures"
    tasks = "/tasks"


def create_temp_pictures_dir():
    path = pathlib.Path(settings.TEMP_PICTURES_DIR)
    if not path.exists():
        path.mkdir()


def save_temp_picture(picture: UploadFile):
    temp_file = uuid.uuid4().hex
    temp_path = f"{settings.TEMP_PICTURES_DIR}/{temp_file}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(picture.file, buffer)
    return temp_path


def delete_temp_picture(picture: str):
    path = pathlib.Path(picture)
    if path.exists():
        path.unlink()


def standardize_pictures(picture: str):
    try:
        image = Image.open(picture, mode="r")
    except UnidentifiedImageError:
        return {"status_code": 400, "detail": "Invalid file type"}
    if image.format not in settings.VALID_PICTURE_FORMATS:
        return {"status_code": 400, "detail": "Invalid picture format"}
    fwidth, fheight = settings.PICTURE_OUTPUT_SIZE
    cwidth, cheight = image.size
    if cwidth < cwidth or cheight < fheight:
        return {"status_code": 400, "detail": "Image is too small"}
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
        fp=f"{settings.PICTURES_DIR}/{name}",
        format=settings.PICTURE_OUTPUT_FORMAT,
    )
    return {"picture": name}
