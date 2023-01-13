from app.utils import standardize_pictures, delete_temp_picture
from app.core.celery import celery_app, celery_log


@celery_app.task
def standardize_picture_task(picture: str):
    celery_log.info(f"Processing {picture} file")
    data = standardize_pictures(picture)
    delete_temp_picture(picture)
    return data
