from fastapi import HTTPException
from sqlmodel import Session, select

from app.db_and_models.models import Post, PostModel, User


def create_post(post: PostModel, db: Session, user_id):
    user = db.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    post = Post(content=post.content, created_at=post.created_at, user_id=user_id)
    db.add(post)
    db.commit()
    return {"success": f"Post mit {post.id} von {user_id} erstellt"}


def delete_post(post_id: int, db: Session, user_id: int):

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    print(user_id, post.user_id)
    if post.user_id != user_id:
        raise HTTPException(
            status_code=401, detail="Not allowed to delete posts of other uses"
        )

    db.delete(post)
    db.commit()
    return {"success": f"Post mit {post_id} gelöscht"}


def update_post(post_id: int, post: PostModel, db: Session, user_id: int):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.user_id != user_id:
        raise HTTPException(
            status_code=401, detail="Not allowed to update posts of other uses"
        )

    update_data = post.dict(exclude_unset=True)
    db_post.update(update_data)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_post(post_id: int, db: Session):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


def get_all_posts_by_user_id(user_id: int, db: Session):
    db_posts = db.query(Post).filter(Post.user_id == user_id).all()
    return db_posts
