from sqlmodel import SQLModel


class AccessTokenRead(SQLModel):
    access_token: str
    token_type: str
