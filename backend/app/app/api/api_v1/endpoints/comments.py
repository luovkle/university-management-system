from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.api.deps import get_current_user, get_session
from app.crud.comment import crud_comment
from app.models import (
    CommentCreate,
    CommentRead,
    CommentReadWithPost,
    CommentUpdate,
    User,
)
from app.models.message import MessageRead
from app.utils import Prefix, Tag

router = APIRouter(prefix=Prefix.comments, tags=[Tag.comments])


@router.post("", response_model=CommentRead, status_code=201)
def create_comment(
    *,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    comment: CommentCreate,
):
    profile_id = current_user.profile.id or 0
    db_comment = crud_comment.create(session, comment, profile_id)
    return db_comment


@router.get("", response_model=list[CommentRead])
def read_comments(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    db_comments = crud_comment.read_all(session, offset, limit)
    return db_comments


@router.get("/{id}", response_model=CommentReadWithPost)
def read_comment(*, session: Session = Depends(get_session), id: int):
    db_comment = crud_comment.read_single(session, id)
    return db_comment


@router.put("/{id}", response_model=CommentRead)
def update_comment(
    *,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    comment: CommentUpdate,
    id: int,
):
    profile_id = current_user.profile.id or 0
    db_comment = crud_comment.update(session, comment, id, profile_id)
    return db_comment


@router.delete("/{id}", response_model=MessageRead)
def delete_comment(
    *,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    id: int,
):
    profile_id = current_user.profile.id or 0
    msg = crud_comment.delete(session, id, profile_id)
    return msg
