from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.deps import DbSession, get_current_user
from app.models.user import User
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.order import OrderCreate, OrderRead
from app.services.order_service import OrderService

router = APIRouter()


def get_order_service(db: DbSession) -> OrderService:
    return OrderService(OrderRepository(db), ProductRepository(db))


@router.post("", response_model=OrderRead, status_code=201)
def create_order(
    payload: OrderCreate,
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
) -> OrderRead:
    return service.create_order(current_user, payload)


@router.get("", response_model=list[OrderRead])
def list_my_orders(
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
) -> list[OrderRead]:
    return service.list_user_orders(current_user.id)


@router.get("/{order_id}", response_model=OrderRead)
def get_order(
    order_id: UUID,
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
) -> OrderRead:
    return service.get_order_for_user(order_id, current_user.id)
