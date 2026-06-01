from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_user_repository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AuthResponse
from app.schemas.user import UserLogin, UserRegister
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_in: UserRegister,
    repository: UserRepository = Depends(get_user_repository),
) -> AuthResponse:
    return AuthService(repository).register(user_in)


@router.post("/login", response_model=AuthResponse)
def login(
    credentials: UserLogin,
    repository: UserRepository = Depends(get_user_repository),
) -> AuthResponse:
    auth = AuthService(repository).login(credentials)
    if auth is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return auth
