from pydantic import BaseModel

from app.schemas.user import UserRead


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead
