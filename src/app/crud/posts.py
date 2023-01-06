from fastapi import HTTPException
from sqlmodel import Session, select

from app.db_and_models.models import Post, PostModel, User


async def create_post(postmodel: PostModel, db: Session, user_id: int):
    user = db.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    post = Post(
        content=postmodel.content, created_at=postmodel.created_at, user_id=user_id
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"success", f"Post mit {post.id} von {user_id} erstellt"}


async def delete_post(post_id: int, db: Session, user_id: int):
    post = db.exec(select(Post).where(Post.id == post_id)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post wurde nicht gefunden")
    if post.user_id != user_id:
        raise HTTPException(status_code=401, detail="Not authorized")
    db.delete(post)
    db.commit()
    return {"success", f"Post mit {post_id} wurde gelöscht!"}


async def update_post(post_id: int, db: Session, user_id: int, postmodel: PostModel):
    post = db.exec(select(Post).where(Post.id == post_id)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post wurde nicht gefunden")
    if post.user_id != user_id:
        raise HTTPException(status_code=401, detail="Not authorized")
    post.created_at = postmodel.created_at
    post.content = postmodel.content
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"success": f"Post mit {post.id} erfolgreich geupdated"}


async def get_post(post_id: int, db: Session):
    post = db.exec(select(Post).where(Post.id == post_id)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post wurde nicht gefunden")
    return post


async def get_all_posts_by_user_id(user_id: int, db: Session):
    posts = db.exec(select(Post).where(Post.user_id == user_id)).all()
    return posts
