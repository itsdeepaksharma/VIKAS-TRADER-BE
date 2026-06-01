from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.order import Order, OrderStatus
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Order)

    def get_by_id(self, order_id: UUID, *, with_buyer: bool = False) -> Order | None:
        stmt = select(Order).options(joinedload(Order.items)).where(Order.id == order_id)
        if with_buyer:
            stmt = stmt.options(joinedload(Order.user))
        return self.db.scalar(stmt)

    def list_for_user(self, user_id: UUID) -> list[Order]:
        return list(
            self.db.scalars(
                select(Order)
                .options(joinedload(Order.items))
                .where(Order.user_id == user_id)
                .order_by(Order.created_at.desc())
            )
            .unique()
            .all()
        )

    def list_all(self, *, status: OrderStatus | None = None, with_buyer: bool = False) -> list[Order]:
        stmt = select(Order).options(joinedload(Order.items)).order_by(Order.created_at.desc())
        if with_buyer:
            stmt = stmt.options(joinedload(Order.user))
        if status:
            stmt = stmt.where(Order.status == status)
        return list(self.db.scalars(stmt).unique().all())

    def count_all(self) -> int:
        from sqlalchemy import func

        return int(self.db.scalar(select(func.count()).select_from(Order)) or 0)

    def count_by_status(self, status: OrderStatus) -> int:
        from sqlalchemy import func

        return int(
            self.db.scalar(
                select(func.count()).select_from(Order).where(Order.status == status)
            )
            or 0
        )

    def count_new(self) -> int:
        return self.count_by_status(OrderStatus.pending) + self.count_by_status(
            OrderStatus.processing
        )
