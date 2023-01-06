from sqlmodel import create_engine
import os

# engine = create_engine(
#     "sqlite:///twitter.db", connect_args={"check_same_thread": False}
# )


DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)