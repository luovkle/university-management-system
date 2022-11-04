from app.core.celery import celery_app, celery_log
from app.crud.picture import crud_picture
from app.utils import delete_temp_picture


@celery_app.task
def standardize_picture_task(picture: str):
    celery_log.info(f"Processing {picture} file")
    data = crud_picture.standardize(picture)
    delete_temp_picture(picture)
    return data
