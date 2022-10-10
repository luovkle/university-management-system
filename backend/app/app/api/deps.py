from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session

from app.core.config import settings
from app.utils import Tag
from app.db.engine import engine
from app.utils import CustomHttpExceptions
from app.crud.user import crud_user

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/{Tag.login}/access-token"
)


def get_session():
    with Session(engine) as session:
        yield session


def get_current_user(
    session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        raise CustomHttpExceptions.credentials_exception
    username = payload.get("sub")
    db_user = crud_user.get_by_username(session, username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user
