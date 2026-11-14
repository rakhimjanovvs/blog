from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from typing import Literal

from schemas import PostCreate, PostRead, CommentCreate, CommentRead
from models import Post, Comment
from database import get_db

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(post_data: PostCreate, db: Session = Depends(get_db)):
    existing_post = db.query(Post).filter_by(title=post_data.title).first()
    if existing_post:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пост с таким названием уже существует"
        )

    new_post = Post(title=post_data.title, body=post_data.body)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/", response_model=list[PostRead])
def get_post(
    sort: Literal["new", "old"] = "new",
    search: str | None = None,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Post)
    if sort == "new":
        query = query.order_by(Post.id.desc())
    elif sort == "old":
        query = query.order_by(Post.id)

    if search:
        query = query.filter(Post.title.ilike(f"%{search}%"))
    return query.offset(offset).limit(limit).all()


@router.post("/{post_id}/comments", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def create_comment(post_id: int, comment_data: CommentCreate, db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")

    new_comment = Comment(text=comment_data.text, post_id=post_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


@router.get("/{post_id}/comments", response_model=list[CommentRead])
def list_comments(post_id: int, db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    return post.comments


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")

    db.delete(post)
    db.commit()