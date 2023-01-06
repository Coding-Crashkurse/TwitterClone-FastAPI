import os

from sqlmodel import create_engine

# engine = create_engine(
#     "sqlite:///twitter.db", connect_args={"check_same_thread": False}
# )

engine = create_engine(os.environ.get("DATABASE_URL"))