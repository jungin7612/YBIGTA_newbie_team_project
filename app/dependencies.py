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
