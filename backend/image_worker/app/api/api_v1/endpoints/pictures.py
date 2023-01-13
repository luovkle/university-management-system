from fastapi import APIRouter, UploadFile

from app.models.task import TaskIDRead
from app.utils import Tag, Prefix, save_temp_picture
from app.celery_worker import standardize_picture_task

router = APIRouter(prefix=Prefix.pictures, tags=[Tag.pictures])


@router.post("", response_model=TaskIDRead)
def send_picture(picture: UploadFile):
    temp_path = save_temp_picture(picture)
    task = standardize_picture_task.delay(temp_path)
    return {"task_id": task.id}
