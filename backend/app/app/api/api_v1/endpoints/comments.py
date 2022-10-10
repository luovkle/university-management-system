from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.api.deps import get_session
from app.models import (
    Comment,
    CommentCreate,
    CommentRead,
    CommentReadWithPost,
)
from app.utils import Tag, Prefix

router = APIRouter(prefix=Prefix.comments, tags=[Tag.comments])


@router.post("", response_model=CommentRead, status_code=201)
def create_comment(*, session: Session = Depends(get_session), comment: CommentCreate):
    db_comment = Comment.from_orm(comment)
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)
    return db_comment


@router.get("", response_model=list[CommentRead])
def read_comments(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    comments = session.exec(select(Comment).offset(offset).limit(limit)).all()
    return comments


@router.get("/{id}", response_model=CommentReadWithPost)
def read_comment(*, session: Session = Depends(get_session), id: int):
    comment = session.get(Comment, id)
    if not comment:
        raise HTTPException(status_code=404)
    return comment
