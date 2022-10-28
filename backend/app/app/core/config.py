import os
import secrets

from pydantic import BaseSettings


class Settings(BaseSettings):
    # App
    APP_TITLE: str = "University Management System"
    APP_LICENSE_NAME: str = "MIT"
    APP_LICENSE_URL: str = "https://opensource.org/licenses/MIT"
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "")

    # Api
    API_V1_STR: str = "/api/v1"

    # Tokens
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    ALGORITHM = "HS256"

    # Schemas / Models
    USERNAME_MIN_LENGTH: int = 3
    USERNAME_MAX_LENGTH: int = 15
    NAME_MIN_LENGTH: int = 1
    NAME_MAX_LENGTH: int = 30
    PASSWORD_MIN_LENGTH: int = 12
    PASSWORD_MAX_LENGTH: int = 72

    POST_TITLE_MIN_LENGTH: int = 5
    POST_TITLE_MAX_LENGTH: int = 50
    POST_SUMMARY_MIN_LENGTH: int = 5
    POST_SUMMARY_MAX_LENGTH: int = 100
    POST_CONTENT_MIN_LENGTH: int = 1
    POST_CONTENT_MAX_LENGTH: int = 5000

    COMMENT_MIN_LENGTH: int = 5
    COMMENT_MAX_LENGTH: int = 100

    PROFILE_DESCRIPTION_MIN_LENGTH: int = 5
    PROFILE_DESCRIPTION_MAX_LENGTH: int = 500

    HOMEWORK_TITLE_MIN_LENGTH: int = POST_TITLE_MIN_LENGTH
    HOMEWORK_TITLE_MAX_LENGTH: int = POST_TITLE_MAX_LENGTH
    HOMEWORK_DESCRIPTION_MIN_LENGTH: int = POST_CONTENT_MIN_LENGTH
    HOMEWORK_DESCRIPTION_MAX_LENGTH: int = POST_CONTENT_MAX_LENGTH

    # DB
    DB_USER: str = os.getenv("POSTGRES_USER", "")
    DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    DB_SERVER: str = os.getenv("POSTGRES_SERVER", "")
    DB_NAME: str = os.getenv("POSTGRES_DB", "")
    DB_URI: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"


settings = Settings()
