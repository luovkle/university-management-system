from fastapi import APIRouter, Depends, File, UploadFile
from app.api.deps import get_current_user

from app.models import User
from app.utils import Tag, Prefix, save_temp_picture
from app.celery_worker import standardize_picture_task

router = APIRouter(prefix=Prefix.pictures, tags=[Tag.pictures])


@router.put("")
def upload_picture(
    current_user: User = Depends(get_current_user), picture: UploadFile = File()
):
    temp_path = save_temp_picture(picture)
    task = standardize_picture_task.delay(temp_path)
    return {"task_id": task.id}
