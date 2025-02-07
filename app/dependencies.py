# from fastapi import Depends
# from app.user.user_repository import UserRepository
# from app.user.user_service import UserService

# def get_user_repository() -> UserRepository:
#     return UserRepository()

# def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
#     return UserService(repo)

from fastapi import Depends
from sqlalchemy.orm import Session
from app.user.user_repository import UserRepository
from app.user.user_service import UserService
from database.mysql_connection import SessionLocal
from database.mongodb_connection import mongo_db


def get_db() -> Session:
    """ SQLAlchemy 세션 생성 및 반환 """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)


def get_mongo_client():
    return mongo_db
