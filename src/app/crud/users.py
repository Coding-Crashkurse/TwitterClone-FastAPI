from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.auth.auth import create_access_token, get_password_hash, verify_password
from app.db_and_models.models import User, UserModel


async def create_user(usermodel: UserModel, db: Session):

    existing_user = db.exec(select(User).where(User.email == usermodel.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use")
    usermodel.password = get_password_hash(usermodel.password)
    user = User.from_orm(usermodel)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"success": f"User mit ID {user.id} erstellt"}


async def login_user(form_data: OAuth2PasswordRequestForm, db: Session):
    existing_user = db.exec(
        select(User).where(User.username == form_data.username)
    ).first()
    if not existing_user:
        raise HTTPException(status_code=401, detail="Not able to be authenticated")
    if not verify_password(form_data.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Not able to be authenticated")
    token = create_access_token(user=existing_user)

    return {"access_token": token, "token_type": "bearer"}
