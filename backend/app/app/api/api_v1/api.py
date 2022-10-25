from fastapi import APIRouter

from app.api.api_v1.endpoints.comments import router as comments_router
from app.api.api_v1.endpoints.login import router as login_router
from app.api.api_v1.endpoints.posts import router as posts_router
from app.api.api_v1.endpoints.users import router as users_router
from app.core.config import settings

api_router = APIRouter(prefix=settings.API_V1_STR)
api_router.include_router(login_router)
api_router.include_router(users_router)
api_router.include_router(posts_router)
api_router.include_router(comments_router)
