from enum import Enum

from fastapi import HTTPException, status


class Tag(str, Enum):
    login = "login"
    users = "users"
    posts = "posts"
    comments = "comments"


class Prefix(str, Enum):
    login = "/login"
    users = "/users"
    posts = "/posts"
    comments = "/comments"


class CustomHttpExceptions:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
