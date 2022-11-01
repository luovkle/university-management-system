from sqlmodel import SQLModel


class PictureRead(SQLModel):
    picture: str
