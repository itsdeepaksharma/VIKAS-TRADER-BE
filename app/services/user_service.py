from fastapi import status

from app.core.exceptions import AppException
from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def create_user(self, user_in: UserCreate) -> User:
        existing_user = self.repository.get_by_email(user_in.email)
        if existing_user:
            raise AppException(
                "A user with this email already exists.",
                status_code=status.HTTP_409_CONFLICT,
                error_code="user_exists",
            )

        user = User(
            email=user_in.email.lower(),
            hashed_password=get_password_hash(user_in.password),
        )
        return self.repository.add(user)
