from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.order import OrderStatus


class OrderItemCreate(BaseModel):
    product_id: UUID
    quantity: int = Field(ge=1, le=99)


class OrderCreate(BaseModel):
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderItemRead(BaseModel):
    id: UUID
    product_id: UUID | None
    product_name: str
    product_image: str
    quantity: int
    unit_price: Decimal

    model_config = ConfigDict(from_attributes=True)


class OrderRead(BaseModel):
    id: UUID
    status: OrderStatus
    payment_method: str
    subtotal: Decimal
    total: Decimal
    shipping_address: str
    created_at: datetime
    items: list[OrderItemRead]

    model_config = ConfigDict(from_attributes=True)


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderBuyerRead(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    phone: str
    address: str

    model_config = ConfigDict(from_attributes=True)


class AdminOrderRead(OrderRead):
    user_id: UUID
    buyer: OrderBuyerRead
