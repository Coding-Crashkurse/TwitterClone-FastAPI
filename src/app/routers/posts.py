from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.auth.auth import get_current_user
from app.crud.posts import (
    create_post,
    delete_post,
    get_post,
    update_post,
    get_all_posts_by_user_id,
)
from app.db_and_models.models import Like, Post, PostModel, User
from app.db_and_models.session import get_session

router = APIRouter(tags=["Posts"])


@router.post("/posts")
def create_post_endpoint(
    post: PostModel,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return create_post(post, db, current_user.id)


@router.get("/posts/{post_id}")
def get_post_endpoint(post_id: int, db: Session = Depends(get_session)):
    return get_post(post_id, db)


@router.delete("/posts/{post_id}")
def delete_post_endpoint(
    post_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return delete_post(post_id, db, user_id=current_user.id)


@router.put("/posts/{post_id}")
def update_post_endpoint(
    post_id: int,
    post: PostModel,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return update_post(post_id, post, db, user_id=current_user.id)


@router.get("/users/{user_id}/posts")
def get_user_posts_endpoint(user_id: int, db: Session = Depends(get_session)):
    return get_all_posts_by_user_id(user_id=user_id, db=db)
