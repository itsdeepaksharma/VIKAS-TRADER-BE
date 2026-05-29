from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class AdminDashboardStats(BaseModel):
    total_users: int
    active_users: int
    admin_users: int
    inactive_users: int
    total_products: int
    out_of_stock_products: int
    low_stock_products: int
    total_orders: int
    new_orders: int


class AdminUserListItem(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    phone: str
    address: str
    is_active: bool
    is_superuser: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AdminUserStatusUpdate(BaseModel):
    is_active: bool
