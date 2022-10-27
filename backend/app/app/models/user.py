from typing import TYPE_CHECKING, Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from app.core.config import settings

if TYPE_CHECKING:
    from .profile import Profile, ProfileRead


class UserBase(SQLModel):
    username: str = Field(
        unique=True,
        index=True,
        min_length=settings.USERNAME_MIN_LENGTH,
        max_length=settings.USERNAME_MAX_LENGTH,
    )
    email: EmailStr = Field(unique=True, index=True)
    first_name: str = Field(
        min_length=settings.NAME_MIN_LENGTH,
        max_length=settings.NAME_MAX_LENGTH,
    )
    last_name: str = Field(
        min_length=settings.NAME_MIN_LENGTH,
        max_length=settings.NAME_MAX_LENGTH,
    )


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str

    profile: "Profile" = Relationship(
        back_populates="user", sa_relationship_kwargs={"uselist": False}
    )


class UserCreate(UserBase):
    password: str = Field(
        min_length=settings.PASSWORD_MIN_LENGTH,
        max_length=settings.PASSWORD_MAX_LENGTH,
    )


class UserRead(UserBase):
    id: int


class UserReadWithProfile(UserRead):
    profile: Optional["ProfileRead"] = None


class UserUpdate(SQLModel):
    username: str | None = Field(
        default=None,
        unique=True,
        min_length=settings.USERNAME_MIN_LENGTH,
        max_length=settings.USERNAME_MAX_LENGTH,
    )
