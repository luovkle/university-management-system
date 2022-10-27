from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from app.api.deps import get_session

from app.utils import Tag, Prefix
from app.crud.profile import crud_profile
from app.models import ProfileRead, ProfileReadWithPosts

router = APIRouter(prefix=Prefix.profiles, tags=[Tag.profiles])


@router.get("", response_model=list[ProfileRead])
def read_profiles(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100)
):
    db_profiles = crud_profile.read_many(session, offset=offset, limit=limit)
    return db_profiles


@router.get("/{id}", response_model=ProfileReadWithPosts)
def read_profile(*, session: Session = Depends(get_session), id: int):
    db_profile = crud_profile.read_single(session, id=id)
    return db_profile
