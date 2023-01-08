import os

from sqlmodel import create_engine

engine = create_engine(
    "sqlite:///twitter.db", connect_args={"check_same_thread": False}
)

# DATABASE_URL = os.environ.get("DATABASE_URL")
# engine = create_engine(DATABASE_URL)

