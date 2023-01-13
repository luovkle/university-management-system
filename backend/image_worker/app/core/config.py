from pydantic import BaseSettings


class Settings(BaseSettings):
    # App
    APP_TITLE: str = "Image Worker"
    APP_LICENSE_NAME: str = "MIT"
    APP_LICENSE_URL: str = "https://opensource.org/licenses/MIT"

    # Api
    API_V1_STR: str = "/api/v1"

    # Pictures
    DEFAULT_PICTURE: str = "default_picture.png"
    VALID_PICTURE_FORMATS: list[str] = ["JPEG", "PNG"]
    PICTURE_OUTPUT_SIZE: list[int] = [800, 800]
    PICTURE_OUTPUT_FORMAT: str = "PNG"
    FILES_DIR: str = "files"
    PICTURES_DIR: str = FILES_DIR + "/pictures"
    TEMP_PICTURES_DIR: str = FILES_DIR + "/temp"


settings = Settings()
