from fastapi import status

from app.core.exceptions import AppException
from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRegister


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def create_user(self, user_in: UserRegister) -> User:
        existing_email = self.repository.get_by_email(user_in.email)
        if existing_email:
            raise AppException(
                "A user with this email already exists.",
                status_code=status.HTTP_409_CONFLICT,
                error_code="email_exists",
            )

        existing_phone = self.repository.get_by_phone(user_in.phone)
        if existing_phone:
            raise AppException(
                "A user with this phone number already exists.",
                status_code=status.HTTP_409_CONFLICT,
                error_code="phone_exists",
            )

        user = User(
            email=user_in.email.lower(),
            hashed_password=get_password_hash(user_in.password),
            first_name=user_in.first_name.strip(),
            last_name=user_in.last_name.strip(),
            phone=user_in.phone.strip(),
            address=user_in.address.strip(),
        )
        return self.repository.add(user)
