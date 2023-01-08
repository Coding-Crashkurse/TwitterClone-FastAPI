import datetime
import os

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from app.db_and_models.models import User
from app.db_and_models.session import get_session

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_IN_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_IN_MINUTES"))



pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(secret=plain_password, hash=hashed_password)


def create_access_token(user: User):
    try:
        claims = {
            "sub": user.username,
            "email": user.email,
            "exp": datetime.datetime.now()
            + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_IN_MINUTES),
        }
        return jwt.encode(claims, key=SECRET_KEY, algorithm=ALGORITHM)
    except JWTError:
        raise JWTError("Wrong Token")


def verify_token(token: str):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except JWTError:
        raise JWTError("Token decoding did not work!")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)
):
    payload = verify_token(token)
    username = payload.get("sub")
    user = db.exec(select(User).where(User.username == username)).first()
    if not user:
        HTTPException(status_code=401, detail="Not authorized")
    return user
