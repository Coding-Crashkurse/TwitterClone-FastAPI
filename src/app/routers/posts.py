from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.auth.auth import get_current_user
from app.crud.posts import (
    create_post,
    delete_post,
    get_all_posts_by_user_id,
    get_post,
    update_post,
)
from app.db_and_models.models import PostModel, User
from app.db_and_models.session import get_session

router = APIRouter(tags=["Posts"])


@router.post("/posts", status_code=201)
async def create_post_endpoint(
    postmodel: PostModel,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await create_post(postmodel=postmodel, db=db, user_id=current_user.id)


@router.delete("/posts/{post_id}", status_code=204)
async def delete_post_endpoint(
    post_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await delete_post(post_id=post_id, db=db, user_id=current_user.id)


@router.put("/posts/{post_id}", status_code=200)
async def update_post_endpoint(
    post_id: int,
    postmodel: PostModel,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await update_post(
        post_id=post_id, db=db, user_id=current_user.id, postmodel=postmodel
    )


@router.get("/posts/{post_id}", status_code=200)
async def get_single_post(post_id: int, db: Session = Depends(get_session)):
    return await get_post(post_id=post_id, db=db)


@router.get("/users/{user_id}/posts/", status_code=200)
async def get_user_posts_endpoint(user_id: int, db: Session = Depends(get_session)):
    return await get_all_posts_by_user_id(user_id=user_id, db=db)
