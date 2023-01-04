from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.auth.auth import create_access_token, get_current_user, verify_password
from app.crud.users import create_user
from app.db_and_models.models import Post, User, UserModel
from app.db_and_models.session import get_session

router = APIRouter(tags=["Users"])


@router.post("/users")
def create_user_endpoint(user: UserModel, db: Session = Depends(get_session)):
    return create_user(user, db)


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)
):
    db_user = db.query(User).filter(User.username == form_data.username).first()
    if not db_user:
        raise HTTPException(
            status_code=401, detail="Anmeldeinformationen nicht korrekt"
        )

    if verify_password(form_data.password, db_user.password):
        token = create_access_token(db_user)
        return {"access_token": token, "token_Type": "bearer"}
    raise HTTPException(status_code=401, detail="Anmeldeinformationen nicht korrekt")
