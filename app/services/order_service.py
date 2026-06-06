from decimal import Decimal
from uuid import UUID

from fastapi import status

from app.core.exceptions import AppException
from app.models.order import Order, OrderItem, OrderStatus
from app.models.user import User
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.schemas.order import AdminOrderRead, OrderBuyerRead, OrderCreate, OrderRead, OrderStatusUpdate
class OrderService:
    def __init__(
        self,
        order_repo: OrderRepository,
        product_repo: ProductRepository,
    ) -> None:
        self.order_repo = order_repo
        self.product_repo = product_repo

    def _to_read(self, order: Order) -> OrderRead:
        return OrderRead.model_validate(order)

    def _to_admin_read(self, order: Order) -> AdminOrderRead:
        user = order.user
        if not user:
            user = UserRepository(self.order_repo.db).get_by_id(order.user_id)
        if not user:
            raise AppException(
                "Buyer not found for this order.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        base = OrderRead.model_validate(order)
        return AdminOrderRead(
            **base.model_dump(),
            user_id=order.user_id,
            buyer=OrderBuyerRead.model_validate(user),
        )

    def create_order(self, user: User, payload: OrderCreate) -> OrderRead:
        line_items: list[tuple] = []
        subtotal = Decimal("0")

        for item in payload.items:
            product = self.product_repo.get_by_id(item.product_id, active_only=True)
            if not product:
                raise AppException(
                    f"Product not found: {item.product_id}",
                    status_code=status.HTTP_404_NOT_FOUND,
                )
            if product.stock_quantity < item.quantity:
                raise AppException(
                    f"Insufficient stock for {product.name}. Available: {product.stock_quantity}",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            line_total = product.price * item.quantity
            subtotal += line_total
            line_items.append((product, item.quantity))

        order = Order(
            user_id=user.id,
            status=OrderStatus.pending,
            payment_method="direct",
            subtotal=subtotal,
            total=subtotal,  # No separate shipping charge; total matches cart subtotal
            shipping_address=user.address,
        )
        self.order_repo.db.add(order)
        self.order_repo.db.flush()

        for product, quantity in line_items:
            self.order_repo.db.add(
                OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    product_name=product.name,
                    product_image=product.image,
                    quantity=quantity,
                    unit_price=product.price,
                )
            )
            product.stock_quantity -= quantity
            self.order_repo.db.add(product)

        self.order_repo.db.commit()
        self.order_repo.db.refresh(order)
        loaded = self.order_repo.get_by_id(order.id)
        return self._to_read(loaded)  # type: ignore[arg-type]

    def list_user_orders(self, user_id: UUID) -> list[OrderRead]:
        orders = self.order_repo.list_for_user(user_id)
        return [self._to_read(o) for o in orders]

    def list_admin_orders(self, *, status: OrderStatus | None = None) -> list[AdminOrderRead]:
        orders = self.order_repo.list_all(status=status, with_buyer=True)
        return [self._to_admin_read(o) for o in orders]

    def update_order_status(self, order_id: UUID, payload: OrderStatusUpdate) -> OrderRead:
        order = self.order_repo.get_by_id(order_id, with_buyer=False)
        if not order:
            raise AppException("Order not found.", status_code=status.HTTP_404_NOT_FOUND)

        if order.status == OrderStatus.cancelled:
            raise AppException("Cannot update a cancelled order.", status_code=status.HTTP_400_BAD_REQUEST)

        if payload.status == OrderStatus.cancelled and order.status != OrderStatus.cancelled:
            for item in order.items:
                if item.product_id:
                    product = self.product_repo.get_by_id(item.product_id)
                    if product:
                        product.stock_quantity += item.quantity
                        self.order_repo.db.add(product)

        order.status = payload.status
        self.order_repo.db.add(order)
        self.order_repo.db.commit()
        self.order_repo.db.refresh(order)
        loaded = self.order_repo.get_by_id(order.id, with_buyer=False)
        return self._to_read(loaded)  # type: ignore[arg-type]

    def update_order_status_admin(
        self, order_id: UUID, payload: OrderStatusUpdate
    ) -> AdminOrderRead:
        order = self.order_repo.get_by_id(order_id, with_buyer=False)
        if not order:
            raise AppException("Order not found.", status_code=status.HTTP_404_NOT_FOUND)

        if order.status == OrderStatus.cancelled:
            raise AppException("Cannot update a cancelled order.", status_code=status.HTTP_400_BAD_REQUEST)

        if payload.status == OrderStatus.cancelled and order.status != OrderStatus.cancelled:
            for item in order.items:
                if item.product_id:
                    product = self.product_repo.get_by_id(item.product_id)
                    if product:
                        product.stock_quantity += item.quantity
                        self.order_repo.db.add(product)

        order.status = payload.status
        self.order_repo.db.add(order)
        self.order_repo.db.commit()
        loaded = self.order_repo.get_by_id(order.id, with_buyer=True)
        return self._to_admin_read(loaded)  # type: ignore[arg-type]

    def get_order(self, order_id: UUID) -> OrderRead:
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise AppException("Order not found.", status_code=status.HTTP_404_NOT_FOUND)
        return self._to_read(order)

    def get_order_for_user(self, order_id: UUID, user_id: UUID) -> OrderRead:
        order = self.order_repo.get_by_id(order_id)
        if not order or order.user_id != user_id:
            raise AppException("Order not found.", status_code=status.HTTP_404_NOT_FOUND)
        return self._to_read(order)
