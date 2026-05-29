from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.product import Product
from app.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Category)

    def get_by_id(self, category_id: UUID) -> Category | None:
        return self.db.get(Category, category_id)

    def get_by_slug(self, slug: str) -> Category | None:
        return self.db.scalar(select(Category).where(Category.slug == slug))

    def list_active(self) -> list[Category]:
        return list(
            self.db.scalars(
                select(Category)
                .where(Category.is_active.is_(True))
                .order_by(Category.sort_order, Category.name)
            ).all()
        )

    def list_all(self) -> list[Category]:
        return list(
            self.db.scalars(select(Category).order_by(Category.sort_order, Category.name)).all()
        )

    def count_products(self, category_id: UUID) -> int:
        return int(
            self.db.scalar(
                select(func.count())
                .select_from(Product)
                .where(Product.category_id == category_id, Product.is_active.is_(True))
            )
            or 0
        )

    def slug_exists(self, slug: str, exclude_id: UUID | None = None) -> bool:
        stmt = select(Category.id).where(Category.slug == slug)
        if exclude_id:
            stmt = stmt.where(Category.id != exclude_id)
        return self.db.scalar(stmt) is not None
