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

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from database.mysql_connection import SessionLocal
from app.user.user_schema import User  # 기존 Pydantic 모델 사용

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User:
        """ 이메일로 유저 조회 """
        query = "SELECT id, name, email, password, created_at FROM users WHERE email = :email"
        result = self.db.execute(query, {"email": email}).fetchone()
        if not result:
            return None
        return User(id=result[0], name=result[1], email=result[2], password=result[3], created_at=str(result[4]))

    def save_user(self, user: User) -> User:
        """ 유저가 존재하면 비밀번호를 업데이트하고, 없으면 새로 저장 """
        
        # 유저 존재 여부 확인
        existing_user = self.get_user_by_email(user.email)

        if existing_user:
            # 기존 유저가 있으면 비밀번호 업데이트
            query = "UPDATE users SET password = :password WHERE email = :email"
            self.db.execute(query, {"password": user.password, "email": user.email})
        else:
            # 기존 유저가 없으면 새 유저 추가
            query = """
            INSERT INTO users (name, email, password) 
            VALUES (:name, :email, :password)
            """
            self.db.execute(query, {"name": user.name, "email": user.email, "password": user.password})
        
        self.db.commit()
        return user

    def delete_user(self, email: str) -> bool:
        """ 이메일로 유저 삭제 """
        query = "DELETE FROM users WHERE email = :email"
        result = self.db.execute(query, {"email": email})
        self.db.commit()
        return result.rowcount > 0

