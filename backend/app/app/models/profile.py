from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel
from app.core.config import settings

if TYPE_CHECKING:
    from .user import User
    from .post import Post, PostRead
    from .comment import Comment


class ProfileBase(SQLModel):
    username: str = Field(
        min_length=settings.USERNAME_MIN_LENGTH,
        max_length=settings.USERNAME_MAX_LENGTH,
    )
    description: str | None = Field(
        default=None,
        min_length=settings.PROFILE_DESCRIPTION_MIN_LENGTH,
        max_length=settings.PROFILE_DESCRIPTION_MAX_LENGTH,
    )
    user_id: int | None = Field(default=None, foreign_key="user.id")


class Profile(ProfileBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    user: Optional["User"] = Relationship(back_populates="profile")
    posts: list["Post"] = Relationship(back_populates="profile")
    comments: list["Comment"] = Relationship(back_populates="profile")


class ProfileRead(ProfileBase):
    id: int


class ProfileReadWithPosts(ProfileRead):
    posts: list["PostRead"] = []


class ProfileUpdate(SQLModel):
    description: str | None = Field(
        default=None,
        min_length=settings.PROFILE_DESCRIPTION_MIN_LENGTH,
        max_length=settings.PROFILE_DESCRIPTION_MAX_LENGTH,
    )
