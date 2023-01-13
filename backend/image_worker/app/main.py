from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.api.api_v1.api import api_router
from app.utils import create_temp_pictures_dir

app = FastAPI(
    title=settings.APP_TITLE,
    license_info={
        "name": settings.APP_LICENSE_NAME,
        "url": settings.APP_LICENSE_URL,
    },
)

app.mount("/pictures", StaticFiles(directory="files/pictures"), name="pictures")


@app.on_event("startup")
def on_startup():
    create_temp_pictures_dir()


app.include_router(api_router)
