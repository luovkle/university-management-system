from fastapi import HTTPException
from sqlmodel import Session, select

from app.models import Comment, CommentCreate


class CRUDComment:
    def create(self, session: Session, comment: CommentCreate):
        db_comment = Comment.from_orm(comment)
        session.add(db_comment)
        session.commit()
        session.refresh(db_comment)
        return db_comment

    def read_all(self, session: Session, offset: int, limit: int):
        db_comments = session.exec(select(Comment).offset(offset).limit(limit)).all()
        return db_comments

    def read_single(self, session: Session, id: int):
        db_comment = session.get(Comment, id)
        if not db_comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        return db_comment


crud_comment = CRUDComment()
