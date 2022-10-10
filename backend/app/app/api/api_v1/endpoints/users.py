from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select

from app.api.deps import get_session
from app.models import User, UserCreate, UserRead, UserReadWithPosts, UserUpdate
from app.utils import Tag, Prefix

router = APIRouter(prefix=Prefix.users, tags=[Tag.users])


@router.post("", response_model=UserRead, status_code=201)
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    existing_user = session.exec(
        select(User).where(User.username == user.username)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username not available"
        )
    existing_email = session.exec(select(User).where(User.email == user.email)).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email not available"
        )
    db_user = User(**user.dict(), hashed_password=f"fake_hashed_{user.password}")
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("", response_model=list[UserRead])
def read_users(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@router.get("/{id}", response_model=UserReadWithPosts)
def read_user(*, session: Session = Depends(get_session), id: int):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404)
    return user


@router.put("/{id}", response_model=UserRead)
def update_user(*, session: Session = Depends(get_session), user: UserUpdate, id: int):
    existing_user = session.exec(
        select(User).where(User.username == user.username)
    ).all()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username not available"
        )
    current_user = session.get(User, id)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(current_user, key, value)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.delete("/{id}")
def delete_user(*, session: Session = Depends(get_session), id: int):
    current_user = session.get(User, id)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    session.delete(current_user)
    session.commit()
    return {"msg": "ok"}
