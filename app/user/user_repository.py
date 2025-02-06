# import json

# from typing import Dict, Optional

# from app.user.user_schema import User
# from app.config import USER_DATA

# class UserRepository:
#     def __init__(self) -> None:
#         self.users: Dict[str, dict] = self._load_users()

#     def _load_users(self) -> Dict[str, Dict]:
#         try:
#             with open(USER_DATA, "r") as f:
#                 return json.load(f)
#         except FileNotFoundError:
#             raise ValueError("File not found")

#     def get_user_by_email(self, email: str) -> Optional[User]:
#         user = self.users.get(email)
#         return User(**user) if user else None

#     def save_user(self, user: User) -> User: 
#         self.users[user.email] = user.model_dump()
#         with open(USER_DATA, "w") as f:
#             json.dump(self.users, f)
#         return user

#     def delete_user(self, user: User) -> User:
#         del self.users[user.email]
#         with open(USER_DATA, "w") as f:
#             json.dump(self.users, f)
#         return user

import traceback
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from database.mysql_connection import SessionLocal
from app.user.user_schema import User  # 기존 Pydantic 모델 사용
from sqlalchemy.sql import text
import logging
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User:
        """ 이메일로 유저 조회 """
        query = text("SELECT username, email, password FROM users WHERE email = :email")
        try:
            result = self.db.execute(query, {"email": email}).fetchone()
            logger.info(f"Query executed: {query}")
            logger.info(f"Result fetched: {result}")

            if result is None:
                logger.info("No result")
                raise HTTPException(status_code=404, detail="User not found")

            return User(username=result[0], email=result[1], password=result[2])

        except Exception as e:
            logger.error(f"Error during database query: {e}\n{traceback.format_exc()}")
            raise HTTPException(status_code=500, detail="Database query failed")

    def save_user(self, user: User) -> User:
        """ 유저가 존재하면 비밀번호를 업데이트하고, 없으면 새로 저장 """
        try:
            try:
                existing_user = self.get_user_by_email(user.email)
            except HTTPException as e:
                if e.status_code == 404:
                    existing_user = None
                else:
                    raise 

            if existing_user:
                query = text("UPDATE users SET password = :password WHERE email = :email")
                self.db.execute(query, {"password": user.password, "email": user.email})
            else:
                query = text("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)")
                self.db.execute(query, {"username": user.username, "email": user.email, "password": user.password})

            self.db.commit()
            return user
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error in save_user: {e}\n{traceback.format_exc()}")
            raise HTTPException(status_code=500, detail="Failed to save user")

    def delete_user(self, email: str) -> bool:
        """ 이메일로 유저 삭제 """
        try:
            query = text("DELETE FROM users WHERE email = :email")
            result = self.db.execute(query, {"email": email})
            self.db.commit()
            return result.rowcount > 0
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error in delete_user: {e}\n{traceback.format_exc()}")
            raise HTTPException(status_code=500, detail="Failed to delete user")
