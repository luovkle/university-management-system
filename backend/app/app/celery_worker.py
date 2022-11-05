from sqlmodel import Session

from app.core.celery import celery_app, celery_log
from app.crud.picture import crud_picture
from app.utils import delete_temp_picture
from app.db.engine import engine


@celery_app.task
def standardize_picture_task(picture: str, profile_id: int):
    celery_log.info(f"Processing {picture} file")
    data = crud_picture.standardize(picture)
    new_picture = data.get("picture")
    if new_picture:
        with Session(engine) as session:
            crud_picture.update(session, profile_id, new_picture)
    delete_temp_picture(picture)
    return data
