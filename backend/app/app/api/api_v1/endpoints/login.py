from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.api.deps import get_session
from app.core.security import create_access_token
from app.crud.user import crud_user
from app.models.token import AccessTokenRead
from app.utils import Prefix, Tag

router = APIRouter(prefix=Prefix.login, tags=[Tag.login])


@router.post("/access-token", response_model=AccessTokenRead)
def login_access_token(
    session: Session = Depends(get_session), form: OAuth2PasswordRequestForm = Depends()
):
    username = form.username
    password = form.password
    db_user = crud_user.authenticate(session, username, password)
    access_token = create_access_token(db_user.username)
    return {"access_token": access_token, "token_type": "Bearer"}
