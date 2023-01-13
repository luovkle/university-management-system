from fastapi import APIRouter

from app.api.api_v1.endpoints.pictures import router as pictures_router
from app.api.api_v1.endpoints.tasks import router as tasks_router
from app.core.config import settings

api_router = APIRouter(prefix=settings.API_V1_STR)
api_router.include_router(pictures_router)
api_router.include_router(tasks_router)
