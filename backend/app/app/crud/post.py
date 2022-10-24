from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models import Post, PostCreate, PostUpdate


class CRUDPost:
    def get_by_title(self, session: Session, title: str):
        db_post = session.exec(select(Post).where(Post.title == title)).first()
        return db_post

    def create(self, session: Session, post: PostCreate, user_id: int):
        if self.get_by_title(session, post.title):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Title not available"
            )
        db_post = Post(**post.dict(), user_id=user_id)
        session.add(db_post)
        session.commit()
        session.refresh(db_post)
        return db_post

    def read_many(self, session: Session, offset: int, limit: int):
        db_posts = session.exec(select(Post).offset(offset).limit(limit)).all()
        return db_posts

    def read_single(self, session: Session, id: int):
        db_post = session.get(Post, id)
        if not db_post:
            raise HTTPException(status_code=404, detail="Post not found")
        return db_post

    def update(self, session: Session, post: PostUpdate, id: int, user_id: int):
        if post.title and self.get_by_title(session, post.title):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Title not available"
            )
        db_post = session.exec(
            select(Post).where(Post.id == id, Post.user_id == user_id)
        ).first()
        if not db_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )
        post_data = post.dict(exclude_unset=True)
        for key, value in post_data.items():
            setattr(db_post, key, value)
        session.add(db_post)
        session.commit()
        session.refresh(db_post)
        return db_post

    def delete(self, session: Session, id: int, user_id: int):
        db_post = session.exec(
            select(Post).where(Post.id == id, Post.user_id == user_id)
        ).first()
        if not db_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )
        session.delete(db_post)
        session.commit()
        return {"msg": "ok"}


crud_post = CRUDPost()
