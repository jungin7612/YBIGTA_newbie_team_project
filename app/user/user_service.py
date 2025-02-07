from app.user.user_repository import UserRepository
from app.user.user_schema import User, UserLogin, UserUpdate
from typing import List, Dict,Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException


class UserService:
    def __init__(self, userRepoitory: UserRepository) -> None:
        self.repo = userRepoitory

    def login(self, user_login: UserLogin) -> User:
        """
        사용자가 제공한 이메일과 비밀번호를 확인하여 로그인합니다.

        Args:
            user_login (UserLogin): 로그인 요청 정보, 이메일(email)과 비밀번호(password)를 포함.

        Returns:
            User: 인증된 사용자 객체. 이메일, 비밀번호, 사용자 이름(username)을 포함.

        Raises:
            ValueError: 사용자를 찾을 수 없는 경우 ("User not found").
            ValueError: 비밀번호가 잘못된 경우 ("Invalid password").
        """
        # 사용자 데이터 로드
        existing_user = self.repo.get_user_by_email(user_login.email)

        # 이메일 및 비밀번호 확인 플래그
        email_signal: bool = False
        pw_signal: bool = False

        if existing_user:
            email_signal = True
            if existing_user.password == user_login.password:  # 기존 검증 방식 유지
                pw_signal = True
                return User(email=existing_user.email, password=existing_user.password, username=existing_user.username)
        
        # 이메일 또는 비밀번호가 일치하지 않을 경우 예외 처리
        if not email_signal:
            raise ValueError("User not found")
        if not pw_signal:
            raise ValueError("Invalid password")

        
        
        
    def register_user(self, new_user: User) -> User:
        """
        새로운 사용자를 등록합니다.

        Args:
            new_user (User): 등록하려는 사용자 객체. 이메일(email), 비밀번호(password), 사용자 이름(username) 등을 포함.

        Returns:
            User: 등록된 사용자 객체.

        Raises:
            ValueError: 사용자가 이미 존재하는 경우 ("User already exists").
        """
        # 이미 존재하는 사용자 확인
        if self.repo.get_user_by_email(new_user.email):
            raise ValueError("User already exists")

        # 사용자 저장
        self.repo.save_user(new_user)

        return new_user

    def delete_user(self, email: str) -> User:
        """
        주어진 이메일을 가진 사용자를 삭제합니다.

        Args:
            email (str): 삭제하려는 사용자의 이메일.

        Returns:
            User: 삭제된 사용자 객체.

        Raises:
            ValueError: 사용자를 찾을 수 없는 경우 ("User not Found").
        """
        # 이메일로 사용자 검색
        deleted_user = self.repo.get_user_by_email(email)
        if not deleted_user:
            raise ValueError("User not Found")
        
        # 사용자 삭제
        self.repo.delete_user(deleted_user)
        return deleted_user

    def update_user_pwd(self, user_update: UserUpdate) -> User:
        ## TODO
        """
        사용자의 이메일을 기반으로 비밀번호를 업데이트합니다.

        Args:
            user_update (UserUpdate): 사용자의 이메일과 새 비밀번호를 포함하는 객체.

        Returns:
            User: 새 비밀번호로 업데이트된 사용자 객체.

        Raises:
            ValueError: 지정된 이메일의 사용자가 존재하지 않을 경우.
        """
        user = self.repo.get_user_by_email(user_update.email)
        if not user:
            raise ValueError("User not Found")
        user.password = user_update.new_password
        self.repo.save_user(user)
        updated_user = self.repo.get_user_by_email(user_update.email)
        return updated_user
        