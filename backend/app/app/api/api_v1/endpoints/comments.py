from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.api.deps import get_session
from app.models import CommentCreate, CommentRead, CommentReadWithPost, CommentUpdate
from app.utils import Tag, Prefix
from app.crud.comment import crud_comment

router = APIRouter(prefix=Prefix.comments, tags=[Tag.comments])


@router.post("", response_model=CommentRead, status_code=201)
def create_comment(*, session: Session = Depends(get_session), comment: CommentCreate):
    db_comment = crud_comment.create(session, comment)
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
    *, session: Session = Depends(get_session), comment: CommentUpdate, id: int
):
    db_comment = crud_comment.update(session, comment, id)
    return db_comment


@router.delete("/{id}")
def delete_comment(*, session: Session = Depends(get_session), id: int):
    msg = crud_comment.delete(session, id)
    return msg
