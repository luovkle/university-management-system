from fastapi import APIRouter, Depends, File, UploadFile
from app.api.deps import get_current_user

from app.models import User
from app.models.picture import PictureRead
from app.utils import Tag, Prefix, save_picture

router = APIRouter(prefix=Prefix.pictures, tags=[Tag.pictures])


@router.post("", response_model=PictureRead)
def upload_picture(
    current_user: User = Depends(get_current_user), picture: UploadFile = File()
):
    response = {"picture": save_picture(picture)}
    return response
