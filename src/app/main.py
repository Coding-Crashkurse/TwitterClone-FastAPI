from fastapi import FastAPI

from app.db_and_models.session import create_db_and_tables, drop_tables
from app.routers.followers import router as follow_router
from app.routers.likes import router as likes_router
from app.routers.posts import router as posts_router
from app.routers.users import router as user_router

app = FastAPI()
app.include_router(follow_router)
app.include_router(user_router)
app.include_router(likes_router)
app.include_router(posts_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# @app.on_event("shutdown")
# def on_shutdown():
#     drop_tables()
