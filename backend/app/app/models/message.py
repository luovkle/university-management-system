from sqlmodel import SQLModel


class MessageRead(SQLModel):
    msg: str
