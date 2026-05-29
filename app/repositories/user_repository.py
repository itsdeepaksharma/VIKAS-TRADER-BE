from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, User)

    def get_by_id(self, user_id: UUID) -> User | None:
        return self.db.scalar(select(User).where(User.id == user_id))

    def get_by_email(self, email: str) -> User | None:
        return self.db.scalar(select(User).where(User.email == email.lower()))

    def get_by_phone(self, phone: str) -> User | None:
        normalized = phone.strip()
        return self.db.scalar(select(User).where(User.phone == normalized))

    def list_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        return list(
            self.db.scalars(
                select(User).order_by(User.created_at.desc()).offset(skip).limit(limit),
            ).all(),
        )

    def count_all(self) -> int:
        return int(self.db.scalar(select(func.count()).select_from(User)) or 0)

    def count_active(self) -> int:
        return int(
            self.db.scalar(
                select(func.count()).select_from(User).where(User.is_active.is_(True)),
            )
            or 0,
        )

    def count_admins(self) -> int:
        return int(
            self.db.scalar(
                select(func.count())
                .select_from(User)
                .where(User.is_superuser.is_(True)),
            )
            or 0,
        )
