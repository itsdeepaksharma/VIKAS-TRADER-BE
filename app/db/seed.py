import structlog
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.user_repository import UserRepository

logger = structlog.get_logger(__name__)


def ensure_admin_user(db: Session, settings: Settings) -> None:
    repository = UserRepository(db)
    existing = repository.get_by_email(settings.admin_email)

    if existing:
        updated = False
        if not existing.is_superuser:
            existing.is_superuser = True
            updated = True
        if not existing.is_active:
            existing.is_active = True
            updated = True
        if settings.app_env in {"local", "development", "test"}:
            existing.hashed_password = get_password_hash(settings.admin_password)
            updated = True
        if updated:
            db.add(existing)
            db.commit()
            logger.info("admin_user_updated", email=settings.admin_email)
        return

    admin = User(
        email=settings.admin_email.lower(),
        hashed_password=get_password_hash(settings.admin_password),
        first_name=settings.admin_first_name,
        last_name=settings.admin_last_name,
        phone=settings.admin_phone,
        address=settings.admin_address,
        is_active=True,
        is_superuser=True,
    )
    repository.add(admin)
    logger.info("admin_user_created", email=settings.admin_email)
