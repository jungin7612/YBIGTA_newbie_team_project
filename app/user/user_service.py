from app.user.user_repository import UserRepository
from app.user.user_schema import User, UserLogin, UserUpdate


class UserService:
    def __init__(self, userRepoitory: UserRepository) -> None:
        self.repo = userRepoitory

    def login(self, user_login: UserLogin) -> User:
        # 사용자 데이터 로드
        
        users_list = self.repo._load_users()

        # 이메일 및 비밀번호 확인 플래그
        email_signal = False
        pw_signal = False

        # 사용자 검색
        for user in users_list.values():  # users_list는 딕셔너리 형태로 로드됩니다
            if user["email"] == user_login.email and user["password"] != user_login.password:
                email_signal = True
            if user["email"] == user_login.email and user["password"] == user_login.password:
                email_signal = True
                pw_signal = True
                # User 객체 생성 및 반환
                return User(email=user["email"], password=user["password"], username=user["username"])

        # 이메일 또는 비밀번호가 일치하지 않을 경우 예외 처리
        if not email_signal:
            raise ValueError("User not found")
        if not pw_signal:
            raise ValueError("Invalid password")
        
        
        
    def register_user(self, new_user: User) -> User:
        ## TODO
        if self.repo.get_user_by_email(new_user.email):
            raise ValueError("User already exists")
        self.repo.save_user(new_user)
        
        return new_user

    def delete_user(self, email: str) -> User:
        ## TODO        
        deleted_user = None
        return deleted_user

    def update_user_pwd(self, user_update: UserUpdate) -> User:
        ## TODO
        updated_user = None
        return updated_user
        