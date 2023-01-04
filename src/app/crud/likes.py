from fastapi import HTTPException
from sqlmodel import Session, select

from app.db_and_models.models import Like, LikeModel, Post, User


def create_like(like: LikeModel, db: Session, user_id: int):
    user = db.exec(select(User).where(User.id == user_id)).first()
    post = db.exec(select(Post).where(Post.id == like.post_id)).first()
    if not user or not post:
        raise HTTPException(status_code=404, detail="User or post not found")

    existing_like = db.exec(
        select(Like).where(Like.user_id == user_id).where(Like.post_id == like.post_id)
    ).first()
    if existing_like:
        raise HTTPException(status_code=400, detail="User has already liked this post")

    like = Like(user_id=user_id, post_id=like.post_id)
    db.add(like)
    db.commit()
    return {"success": "Like added"}


def delete_like(like_id: int, db: Session, user_id: int):
    like = db.exec(select(Like).where(Like.id == like_id)).first()
    if like.user_id != user_id:
        raise HTTPException(status_code=401, detail="Nur eigene Likes löschen erlaubt")
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")

    db.delete(like)
    db.commit()
    return {"success": "Like removed"}


def get_likes_of_post(post_id: int, db: Session):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    likes = db.query(Like).filter(Like.post_id == post_id).all()
    return likes
