from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_user_repository
from app.repositories.user_repository import UserRepository
from app.schemas.token import Token
from app.schemas.user import UserLogin
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    credentials: UserLogin,
    repository: UserRepository = Depends(get_user_repository),
) -> Token:
    token = AuthService(repository).authenticate(
        credentials.email,
        credentials.password,
    )
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return token
