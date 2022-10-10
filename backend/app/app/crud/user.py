from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models import User, UserCreate, UserUpdate
from app.core.security import get_password_hash


class CRUDUser:
    def get_by_username(self, session: Session, username: str):
        db_user = session.exec(select(User).where(User.username == username)).first()
        return db_user

    def get_by_email(self, session: Session, email: str):
        db_user = session.exec(select(User).where(User.email == email)).first()
        return db_user

    def create(self, session: Session, user: UserCreate):
        if self.get_by_username(session, user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username not available"
            )
        if self.get_by_email(session, user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email not available"
            )
        hashed_password = get_password_hash(user.password)
        db_user = User(**user.dict(), hashed_password=hashed_password)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    def read_single(self, session: Session, id: int):
        db_user = session.get(User, id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return db_user

    def read_many(self, session: Session, offset: int, limit: int):
        db_users = session.exec(select(User).offset(offset).limit(limit)).all()
        return db_users

    def update(self, session: Session, user: UserUpdate, id: int):
        if user.username and self.get_by_username(session, user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username not available"
            )
        db_user = session.get(User, id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_user, key, value)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    def delete(self, session: Session, id: int):
        db_user = session.get(User, id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        session.delete(db_user)
        session.commit()
        return {"msg": "ok"}


crud_user = CRUDUser()
