from fastapi import HTTPException
from sqlmodel import Session, select

from app.auth.auth import get_password_hash
from app.db_and_models.models import User, UserModel


def create_user(usermodel: UserModel, db: Session):
    existing_user = db.exec(select(User).where(User.email == usermodel.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use")
    usermodel.password = get_password_hash(usermodel.password)
    user = User.from_orm(usermodel)
    db.add(user)
    db.commit()
    return {"success": f"User mit {user.id} erstellt"}
