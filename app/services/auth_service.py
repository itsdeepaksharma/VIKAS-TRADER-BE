from fastapi import status

from app.core.exceptions import AppException
from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AuthResponse
from app.schemas.user import UserLogin, UserRegister
from app.services.user_service import UserService


class AuthService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository
        self.user_service = UserService(user_repository)

    def register(self, user_in: UserRegister) -> AuthResponse:
        user = self.user_service.create_user(user_in)
        return self._build_auth_response(user)

    def login(self, credentials: UserLogin) -> AuthResponse | None:
        user = self.user_repository.get_by_email(credentials.email)
        if not user or not verify_password(credentials.password, user.hashed_password):
            return None
        if not user.is_active:
            raise AppException(
                "Account is inactive. Contact support.",
                status_code=status.HTTP_403_FORBIDDEN,
                error_code="account_inactive",
            )
        return self._build_auth_response(user)

    def _build_auth_response(self, user: User) -> AuthResponse:
        from app.schemas.user import UserRead

        return AuthResponse(
            access_token=create_access_token(str(user.id)),
            user=UserRead.model_validate(user),
        )
