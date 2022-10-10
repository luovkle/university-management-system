from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.api.deps import get_session
from app.models import UserCreate, UserRead, UserReadWithPosts, UserUpdate
from app.utils import Tag, Prefix
from app.crud.user import crud_user

router = APIRouter(prefix=Prefix.users, tags=[Tag.users])


@router.post("", response_model=UserRead, status_code=201)
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    db_user = crud_user.create(session, user)
    return db_user


@router.get("", response_model=list[UserRead])
def read_users(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    db_users = crud_user.read_many(session, offset, limit)
    return db_users


@router.get("/{id}", response_model=UserReadWithPosts)
def read_user(*, session: Session = Depends(get_session), id: int):
    db_user = crud_user.read_single(session, id)
    return db_user


@router.put("/{id}", response_model=UserRead)
def update_user(*, session: Session = Depends(get_session), user: UserUpdate, id: int):
    db_user = crud_user.update(session, user, id)
    return db_user


@router.delete("/{id}")
def delete_user(*, session: Session = Depends(get_session), id: int):
    msg = crud_user.delete(session, id)
    return msg
