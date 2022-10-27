from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.core.config import settings

if TYPE_CHECKING:
    from .post import Post, PostRead
    from .profile import Profile


class CommentBase(SQLModel):
    content: str = Field(
        min_length=settings.COMMENT_MIN_LENGTH,
        max_length=settings.COMMENT_MAX_LENGTH,
    )
    post_id: int


class Comment(CommentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    profile_id: int | None = Field(default=None, foreign_key="profile.id")
    post_id: int | None = Field(default=None, foreign_key="post.id")

    profile: Optional["Profile"] = Relationship(back_populates="comments")
    post: Optional["Post"] | None = Relationship(back_populates="comments")


class CommentCreate(CommentBase):
    ...


class CommentRead(CommentBase):
    id: int
    profile_id: int


class CommentReadWithPost(CommentRead):
    post: Optional["PostRead"] = None


class CommentUpdate(SQLModel):
    content: str | None = Field(
        default=None,
        min_length=settings.COMMENT_MIN_LENGTH,
        max_length=settings.COMMENT_MAX_LENGTH,
    )
