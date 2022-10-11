from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.api.deps import get_session, get_current_user
from app.models import UserCreate, UserRead, UserReadWithPosts, UserUpdate, User
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
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    db_users = crud_user.read_many(session, offset, limit)
    return db_users


@router.get("/me", response_model=UserReadWithPosts)
def read_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserRead)
def update_user(
    *,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    user: UserUpdate,
):
    id = current_user.id or 0
    db_user = crud_user.update(session, user, id)
    return db_user


@router.delete("/me")
def delete_user(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    id = current_user.id or 0
    msg = crud_user.delete(session, id)
    return msg
