from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models import Profile, ProfileUpdate


class CRUDProfile:
    def read_single(self, session: Session, id: int):
        db_profile = session.get(Profile, id)
        if not db_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
            )
        return db_profile

    def read_many(self, session: Session, offset: int, limit: int):
        db_profiles = session.exec(select(Profile).offset(offset).limit(limit)).all()
        return db_profiles

    def update(self, session: Session, profile: ProfileUpdate, id: int):
        db_profile = session.get(Profile, id)
        if not db_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
            )
        profile_data = profile.dict(exclude_unset=True)
        for key, value in profile_data.items():
            setattr(db_profile, key, value)
        session.add(db_profile)
        session.commit()
        session.refresh(db_profile)
        return db_profile


crud_profile = CRUDProfile()
