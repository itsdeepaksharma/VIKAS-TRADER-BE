from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.category import Category
from app.models.product import Product
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Product)

    def get_by_id(self, product_id: UUID, *, active_only: bool = False) -> Product | None:
        stmt = (
            select(Product)
            .options(joinedload(Product.category))
            .where(Product.id == product_id)
        )
        if active_only:
            stmt = stmt.where(Product.is_active.is_(True))
        return self.db.scalar(stmt)

    def list_active(
        self,
        *,
        category_slug: str | None = None,
        best_sellers: bool = False,
        search: str | None = None,
        newest: bool = False,
    ) -> list[Product]:
        stmt = (
            select(Product)
            .options(joinedload(Product.category))
            .where(Product.is_active.is_(True))
        )
        if category_slug:
            stmt = stmt.join(Category).where(Category.slug == category_slug)
        if best_sellers:
            stmt = stmt.where(Product.is_best_seller.is_(True))
        if search:
            term = f"%{search.strip().lower()}%"
            stmt = stmt.where(Product.name.ilike(term))
        if newest:
            stmt = stmt.order_by(Product.created_at.desc())
        else:
            stmt = stmt.order_by(Product.name)
        return list(self.db.scalars(stmt).unique().all())

    def list_all(self) -> list[Product]:
        return list(
            self.db.scalars(
                select(Product).options(joinedload(Product.category)).order_by(Product.name)
            )
            .unique()
            .all()
        )

    def count_active(self) -> int:
        from sqlalchemy import func

        return int(
            self.db.scalar(
                select(func.count()).select_from(Product).where(Product.is_active.is_(True))
            )
            or 0
        )

    def count_low_stock(self, threshold: int = 5) -> int:
        """Active products with stock between 1 and threshold - 1 (excludes out of stock)."""
        from sqlalchemy import func

        return int(
            self.db.scalar(
                select(func.count())
                .select_from(Product)
                .where(
                    Product.is_active.is_(True),
                    Product.stock_quantity > 0,
                    Product.stock_quantity < threshold,
                )
            )
            or 0
        )

    def count_out_of_stock(self) -> int:
        from sqlalchemy import func

        return int(
            self.db.scalar(
                select(func.count())
                .select_from(Product)
                .where(Product.is_active.is_(True), Product.stock_quantity <= 0)
            )
            or 0
        )
