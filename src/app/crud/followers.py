from fastapi import HTTPException
from sqlmodel import Session, select

from app.db_and_models.models import Follower, FollowerModel, User


def create_follower(follower: FollowerModel, db: Session, user_id: int):
    current_user = db.exec(select(User).where(User.id == user_id)).first()
    followed_user = db.exec(select(User).where(User.id == follower.follower_id)).first()
    if not current_user or not followed_user:
        raise HTTPException(status_code=404, detail="User or followed user not found")

    already_following = db.exec(
        select(Follower)
        .where(Follower.user_id == user_id)
        .where(Follower.follower_id == follower.follower_id)
    ).first()
    if already_following:
        raise HTTPException(
            status_code=404,
            detail=f"User {user_id} folgt {follower.follower_id} bereits",
        )

    new_follower = Follower(user_id=user_id, follower_id=follower.follower_id)
    db.add(new_follower)
    db.commit()
    return {"success": "Follow added"}


def get_following(user_id: int, db: Session):
    followers = db.exec(select(Follower).where(Follower.follower_id == user_id)).all()

    if not followers:
        raise HTTPException(status_code=404, detail="No followers found for this user")
    return followers
