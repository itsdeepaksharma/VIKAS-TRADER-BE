from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.api.deps import DbSession, get_current_admin, get_user_repository
from app.models.order import OrderStatus
from app.models.user import User
from app.repositories.category_repository import CategoryRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.schemas.admin import AdminDashboardStats, AdminUserListItem, AdminUserStatusUpdate
from app.schemas.catalog import (
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
    ProductCreate,
    ProductRead,
    ProductUpdate,
)
from app.schemas.order import AdminOrderRead, OrderStatusUpdate
from app.services.admin_service import AdminService
from app.services.catalog_service import CatalogService
from app.services.order_service import OrderService

router = APIRouter()


def get_catalog_service(db: DbSession) -> CatalogService:
    return CatalogService(CategoryRepository(db), ProductRepository(db))


def get_order_service(db: DbSession) -> OrderService:
    return OrderService(OrderRepository(db), ProductRepository(db))


@router.get("/dashboard", response_model=AdminDashboardStats)
def admin_dashboard(
    db: DbSession,
    _: User = Depends(get_current_admin),
    repository: UserRepository = Depends(get_user_repository),
) -> AdminDashboardStats:
    return AdminService(
        repository,
        ProductRepository(db),
        OrderRepository(db),
    ).get_dashboard_stats()


@router.get("/users", response_model=list[AdminUserListItem])
def list_users(
    _: User = Depends(get_current_admin),
    repository: UserRepository = Depends(get_user_repository),
) -> list[AdminUserListItem]:
    return AdminService(repository).list_users()


@router.patch("/users/{user_id}/status", response_model=AdminUserListItem)
def update_user_status(
    user_id: UUID,
    payload: AdminUserStatusUpdate,
    _: User = Depends(get_current_admin),
    repository: UserRepository = Depends(get_user_repository),
) -> AdminUserListItem:
    user = AdminService(repository).update_user_status(user_id, payload)
    return AdminUserListItem.model_validate(user)


# --- Categories ---


@router.get("/categories", response_model=list[CategoryRead])
def admin_list_categories(
    _: User = Depends(get_current_admin),
    service: CatalogService = Depends(get_catalog_service),
) -> list[CategoryRead]:
    return service.list_categories(admin=True)


@router.post("/categories", response_model=CategoryRead, status_code=201)
def admin_create_category(
    payload: CategoryCreate,
    _: User = Depends(get_current_admin),
    service: CatalogService = Depends(get_catalog_service),
) -> CategoryRead:
    return service.create_category(payload)


@router.patch("/categories/{category_id}", response_model=CategoryRead)
def admin_update_category(
    category_id: UUID,
    payload: CategoryUpdate,
    _: User = Depends(get_current_admin),
    service: CatalogService = Depends(get_catalog_service),
) -> CategoryRead:
    return service.update_category(category_id, payload)


@router.delete("/categories/{category_id}", status_code=204)
def admin_delete_category(
    category_id: UUID,
    _: User = Depends(get_current_admin),
    service: CatalogService = Depends(get_catalog_service),
) -> None:
    service.delete_category(category_id)


# --- Products ---


@router.get("/products", response_model=list[ProductRead])
def admin_list_products(
    _: User = Depends(get_current_admin),
    service: CatalogService = Depends(get_catalog_service),
) -> list[ProductRead]:
    return service.list_products(admin=True)


@router.post("/products", response_model=ProductRead, status_code=201)
def admin_create_product(
    payload: ProductCreate,
    _: User = Depends(get_current_admin),
    service: CatalogService = Depends(get_catalog_service),
) -> ProductRead:
    return service.create_product(payload)


@router.patch("/products/{product_id}", response_model=ProductRead)
def admin_update_product(
    product_id: UUID,
    payload: ProductUpdate,
    _: User = Depends(get_current_admin),
    service: CatalogService = Depends(get_catalog_service),
) -> ProductRead:
    return service.update_product(product_id, payload)


@router.delete("/products/{product_id}", status_code=204)
def admin_delete_product(
    product_id: UUID,
    _: User = Depends(get_current_admin),
    service: CatalogService = Depends(get_catalog_service),
) -> None:
    service.delete_product(product_id)


# --- Orders ---


@router.get("/orders", response_model=list[AdminOrderRead])
def admin_list_orders(
    status: OrderStatus | None = Query(default=None),
    _: User = Depends(get_current_admin),
    service: OrderService = Depends(get_order_service),
) -> list[AdminOrderRead]:
    return service.list_admin_orders(status=status)


@router.patch("/orders/{order_id}/status", response_model=AdminOrderRead)
def admin_update_order_status(
    order_id: UUID,
    payload: OrderStatusUpdate,
    _: User = Depends(get_current_admin),
    service: OrderService = Depends(get_order_service),
) -> AdminOrderRead:
    return service.update_order_status_admin(order_id, payload)
