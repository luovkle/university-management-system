from fastapi import FastAPI

from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_TITLE,
    license_info={
        "name": settings.APP_LICENSE_NAME,
        "url": settings.APP_LICENSE_URL,
    },
)
app.include_router(api_router)
