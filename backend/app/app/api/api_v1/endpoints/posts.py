from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.api.deps import get_session
from app.models import PostCreate, PostRead, PostReadWithComments, PostUpdate
from app.utils import Tag, Prefix
from app.crud.post import crud_post

router = APIRouter(prefix=Prefix.posts, tags=[Tag.posts])


@router.post("", response_model=PostRead, status_code=201)
def create_post(*, session: Session = Depends(get_session), post: PostCreate):
    db_post = crud_post.create(session, post)
    return db_post


@router.get("", response_model=list[PostRead])
def read_posts(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    db_posts = crud_post.read_many(session, offset, limit)
    return db_posts


@router.get("/{id}", response_model=PostReadWithComments)
def read_post(*, session: Session = Depends(get_session), id: int):
    db_post = crud_post.read_single(session, id)
    return db_post


@router.put("/{id}", response_model=PostRead)
def update_post(*, session: Session = Depends(get_session), post: PostUpdate, id: int):
    db_post = crud_post.update(session, post, id)
    return db_post


@router.delete("/{id}")
def delete_post(*, session: Session = Depends(get_session), id: int):
    msg = crud_post.delete(session, id)
    return msg
