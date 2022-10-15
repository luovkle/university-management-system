from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models import Comment, CommentCreate, CommentUpdate, Post


class CRUDComment:
    def create(self, session: Session, comment: CommentCreate, user_id: int):
        if not session.get(Post, comment.post_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )
        db_comment = Comment(**comment.dict(), user_id=user_id)
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

    def update(self, session: Session, comment: CommentUpdate, id: int, user_id: int):
        db_comment = session.exec(
            select(Comment).where(Comment.id == id, Comment.user_id == user_id)
        ).first()
        if not db_comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        comment_data = comment.dict(exclude_unset=True)
        for key, value in comment_data.items():
            setattr(db_comment, key, value)
        session.add(db_comment)
        session.commit()
        session.refresh(db_comment)
        return db_comment

    def delete(self, session: Session, id: int, user_id: int):
        db_comment = session.exec(
            select(Comment).where(Comment.id == id, Comment.user_id == user_id)
        ).first()
        if not db_comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        session.delete(db_comment)
        session.commit()
        return {"msg": "ok"}


crud_comment = CRUDComment()
