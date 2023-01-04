from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.auth.auth import get_current_user
from app.crud.likes import create_like, delete_like, get_likes_of_post
from app.db_and_models.models import Like, LikeModel, Post, User
from app.db_and_models.session import get_session

router = APIRouter(tags=["Likes"])


@router.post("/likes")
def create_like_endpoint(
    like: LikeModel,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return create_like(like, db, current_user.id)


@router.delete("/likes/{like_id}")
def delete_like_endpoint(
    like_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return delete_like(like_id, db, user_id=current_user.id)


@router.get("/posts/{post_id}/likes")
def get_post_likes(post_id: int, db: Session = Depends(get_session)):
    return get_likes_of_post(post_id, db)
