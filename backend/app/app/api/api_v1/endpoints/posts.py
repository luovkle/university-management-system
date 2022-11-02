from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.api.deps import get_current_user, get_session
from app.crud.post import crud_post
from app.models import PostCreate, PostRead, PostReadWithComments, PostUpdate, User
from app.models.message import MessageRead
from app.utils import Prefix, Tag

router = APIRouter(prefix=Prefix.posts, tags=[Tag.posts])


@router.post("", response_model=PostRead, status_code=201)
def create_post(
    *,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    post: PostCreate,
):
    profile_id = current_user.profile.id or 0
    db_post = crud_post.create(session, post, profile_id)
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
def update_post(
    *,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    post: PostUpdate,
    id: int,
):
    profile_id = current_user.profile.id or 0
    db_post = crud_post.update(session, post, id, profile_id)
    return db_post


@router.delete("/{id}", response_model=MessageRead)
def delete_post(
    *,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    id: int,
):
    profile_id = current_user.profile.id or 0
    msg = crud_post.delete(session, id, profile_id)
    return msg
