from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select

from app.api.deps import get_session
from app.models import Post, PostCreate, PostRead, PostReadWithComments, PostUpdate
from app.utils import Tag, Prefix

router = APIRouter(prefix=Prefix.posts, tags=[Tag.posts])


@router.post("", response_model=PostRead, status_code=201)
def create_post(*, session: Session = Depends(get_session), post: PostCreate):
    db_post = Post.from_orm(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@router.get("", response_model=list[PostRead])
def read_posts(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    posts = session.exec(select(Post).offset(offset).limit(limit)).all()
    return posts


@router.get("/{id}", response_model=PostReadWithComments)
def read_post(*, session: Session = Depends(get_session), id: int):
    post = session.get(Post, id)
    if not post:
        raise HTTPException(status_code=404)
    return post


@router.put("/{id}", response_model=PostRead)
def update_post(*, session: Session = Depends(get_session), post: PostUpdate, id: int):
    existing_post = session.exec(select(Post).where(Post.title == post.title)).first()
    if existing_post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Title not available"
        )
    db_post = session.get(Post, id)
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
