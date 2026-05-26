from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_user_repository
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter()


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.post("", response_model=UserRead, status_code=201)
def create_user(
    user_in: UserCreate,
    repository: UserRepository = Depends(get_user_repository),
) -> User:
    return UserService(repository).create_user(user_in)
