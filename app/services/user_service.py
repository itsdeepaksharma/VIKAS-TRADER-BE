from fastapi import status

from app.core.exceptions import AppException
from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRegister, UserUpdate


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

    def update_user(self, user: User, payload: UserUpdate) -> User:
        if payload.first_name is not None:
            user.first_name = payload.first_name.strip()
        if payload.last_name is not None:
            user.last_name = payload.last_name.strip()
        if payload.phone is not None:
            phone = payload.phone.strip()
            existing = self.repository.get_by_phone(phone)
            if existing and existing.id != user.id:
                raise AppException(
                    "A user with this phone number already exists.",
                    status_code=status.HTTP_409_CONFLICT,
                )
            user.phone = phone
        if payload.address is not None:
            user.address = payload.address.strip()

        self.repository.db.add(user)
        self.repository.db.commit()
        self.repository.db.refresh(user)
        return user
