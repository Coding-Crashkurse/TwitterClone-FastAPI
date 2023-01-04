from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.crud.followers import create_follower, get_following
from app.db_and_models.models import FollowerModel, User, FollowerResponseModel
from app.db_and_models.session import get_session
from app.auth.auth import get_current_user


router = APIRouter(tags=["Followers"])


@router.post("/followers")
def create_follower_endpoint(
    follower: FollowerModel,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return create_follower(follower, db, current_user.id)


@router.get("/followers/{user_id}", response_model=list[FollowerResponseModel])
def get_followers(user_id: int, db: Session = Depends(get_session)):
    return get_following(user_id, db)
