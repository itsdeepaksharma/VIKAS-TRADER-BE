from app.core.security import create_access_token, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.token import Token


class AuthService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def authenticate(self, email: str, password: str) -> Token | None:
        user = self.user_repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        return Token(access_token=create_access_token(str(user.id)))
