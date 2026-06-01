from uuid import UUID

from fastapi import status

from app.core.exceptions import AppException
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.schemas.admin import AdminDashboardStats, AdminUserListItem, AdminUserStatusUpdate
from app.models.user import User


class AdminService:
    def __init__(
        self,
        repository: UserRepository,
        product_repo: ProductRepository | None = None,
        order_repo: OrderRepository | None = None,
    ) -> None:
        self.repository = repository
        self.product_repo = product_repo
        self.order_repo = order_repo

    def get_dashboard_stats(self) -> AdminDashboardStats:
        total = self.repository.count_all()
        active = self.repository.count_active()
        admins = self.repository.count_admins()
        products = self.product_repo.count_active() if self.product_repo else 0
        out_of_stock = self.product_repo.count_out_of_stock() if self.product_repo else 0
        low_stock = self.product_repo.count_low_stock() if self.product_repo else 0
        total_orders = self.order_repo.count_all() if self.order_repo else 0
        new_orders = self.order_repo.count_new() if self.order_repo else 0
        return AdminDashboardStats(
            total_users=total,
            active_users=active,
            admin_users=admins,
            inactive_users=total - active,
            total_products=products,
            out_of_stock_products=out_of_stock,
            low_stock_products=low_stock,
            total_orders=total_orders,
            new_orders=new_orders,
        )

    def list_users(self) -> list[AdminUserListItem]:
        users = self.repository.list_all(limit=500)
        return [AdminUserListItem.model_validate(user) for user in users]

    def update_user_status(self, user_id: UUID, payload: AdminUserStatusUpdate) -> User:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise AppException("User not found.", status_code=status.HTTP_404_NOT_FOUND)

        if user.is_superuser and not payload.is_active:
            raise AppException(
                "Cannot deactivate an admin account.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        user.is_active = payload.is_active
        self.repository.db.add(user)
        self.repository.db.commit()
        self.repository.db.refresh(user)
        return user
