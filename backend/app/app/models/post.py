from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.core.config import settings

if TYPE_CHECKING:
    from .comment import Comment, CommentRead
    from .user import User


class PostBase(SQLModel):
    title: str = Field(
        unique=True,
        index=True,
        min_length=settings.POST_TITLE_MIN_LENGTH,
        max_length=settings.POST_TITLE_MAX_LENGTH,
    )
    # tags
    summary: str | None = Field(
        default=None,
        min_length=settings.POST_SUMMARY_MIN_LENGTH,
        max_length=settings.POST_SUMMARY_MAX_LENGTH,
    )
    content: str = Field(
        min_length=settings.POST_CONTENT_MIN_LENGTH,
        max_length=settings.POST_CONTENT_MAX_LENGTH,
    )


class Post(PostBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")

    user: Optional["User"] = Relationship(back_populates="posts")
    comments: list["Comment"] = Relationship(back_populates="post")


class PostCreate(PostBase):
    ...


class PostRead(PostBase):
    id: int
    user_id: int


class PostReadWithComments(PostRead):
    id: int
    user_id: int
    comments: list["CommentRead"] = []


class PostUpdate(SQLModel):
    title: str | None = Field(
        default=None,
        unique=True,
        min_length=settings.POST_TITLE_MIN_LENGTH,
        max_length=settings.POST_TITLE_MAX_LENGTH,
    )
    summary: str | None = Field(
        default=None,
        min_length=settings.POST_SUMMARY_MIN_LENGTH,
        max_length=settings.POST_SUMMARY_MAX_LENGTH,
    )
    content: str | None = Field(
        default=None,
        min_length=settings.POST_CONTENT_MIN_LENGTH,
        max_length=settings.POST_CONTENT_MAX_LENGTH,
    )
