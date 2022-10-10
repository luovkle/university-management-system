from fastapi import FastAPI

from app.api.api_v1.api import api_router
from app.db.base import SQLModel
from app.db.engine import engine

app = FastAPI()


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


app.include_router(api_router)
