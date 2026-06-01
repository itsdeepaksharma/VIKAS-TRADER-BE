from uuid import UUID

from fastapi import status

from app.core.exceptions import AppException
from app.models.category import Category
from app.models.product import Product
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.catalog import (
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
    ProductCreate,
    ProductRead,
    ProductUpdate,
)
from app.services.catalog_mapper import category_to_read, product_to_read


class CatalogService:
    def __init__(
        self,
        category_repo: CategoryRepository,
        product_repo: ProductRepository,
    ) -> None:
        self.category_repo = category_repo
        self.product_repo = product_repo

    def list_categories(self, *, admin: bool = False) -> list[CategoryRead]:
        categories = (
            self.category_repo.list_all() if admin else self.category_repo.list_active()
        )
        return [
            category_to_read(
                cat,
                self.category_repo.count_products(cat.id) if not admin else self._product_count(cat.id),
            )
            for cat in categories
        ]

    def _product_count(self, category_id: UUID) -> int:
        from sqlalchemy import func, select

        from app.models.product import Product

        return int(
            self.category_repo.db.scalar(
                select(func.count()).select_from(Product).where(Product.category_id == category_id)
            )
            or 0
        )

    def get_category_by_slug(self, slug: str) -> CategoryRead:
        category = self.category_repo.get_by_slug(slug)
        if not category or not category.is_active:
            raise AppException("Category not found.", status_code=status.HTTP_404_NOT_FOUND)
        return category_to_read(category, self.category_repo.count_products(category.id))

    def list_products(
        self,
        *,
        category_slug: str | None = None,
        best_sellers: bool = False,
        search: str | None = None,
        newest: bool = False,
        admin: bool = False,
    ) -> list[ProductRead]:
        if admin:
            products = self.product_repo.list_all()
        else:
            products = self.product_repo.list_active(
                category_slug=category_slug,
                best_sellers=best_sellers,
                search=search,
                newest=newest,
            )
        return [product_to_read(p) for p in products]

    def get_product(self, product_id: UUID, *, admin: bool = False) -> ProductRead:
        product = self.product_repo.get_by_id(product_id, active_only=not admin)
        if not product:
            raise AppException("Product not found.", status_code=status.HTTP_404_NOT_FOUND)
        return product_to_read(product)

    def create_category(self, payload: CategoryCreate) -> CategoryRead:
        slug = payload.slug.strip().lower()
        if self.category_repo.slug_exists(slug):
            raise AppException("Category slug already exists.", status_code=status.HTTP_409_CONFLICT)
        category = Category(
            slug=slug,
            name=payload.name.strip(),
            image=payload.image,
            bg_color=payload.bg_color,
            sort_order=payload.sort_order,
            is_active=payload.is_active,
        )
        self.category_repo.add(category)
        return category_to_read(category, 0)

    def update_category(self, category_id: UUID, payload: CategoryUpdate) -> CategoryRead:
        category = self.category_repo.get_by_id(category_id)
        if not category:
            raise AppException("Category not found.", status_code=status.HTTP_404_NOT_FOUND)

        if payload.slug is not None:
            slug = payload.slug.strip().lower()
            if self.category_repo.slug_exists(slug, exclude_id=category_id):
                raise AppException(
                    "Category slug already exists.",
                    status_code=status.HTTP_409_CONFLICT,
                )
            category.slug = slug
        if payload.name is not None:
            category.name = payload.name.strip()
        if payload.image is not None:
            category.image = payload.image
        if payload.bg_color is not None:
            category.bg_color = payload.bg_color
        if payload.sort_order is not None:
            category.sort_order = payload.sort_order
        if payload.is_active is not None:
            category.is_active = payload.is_active

        self.category_repo.db.add(category)
        self.category_repo.db.commit()
        self.category_repo.db.refresh(category)
        return category_to_read(category, self._product_count(category.id))

    def delete_category(self, category_id: UUID) -> None:
        category = self.category_repo.get_by_id(category_id)
        if not category:
            raise AppException("Category not found.", status_code=status.HTTP_404_NOT_FOUND)
        if self._product_count(category_id) > 0:
            raise AppException(
                "Cannot delete category with products. Remove or reassign products first.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        self.category_repo.delete(category)

    def create_product(self, payload: ProductCreate) -> ProductRead:
        category = self.category_repo.get_by_id(payload.category_id)
        if not category:
            raise AppException("Category not found.", status_code=status.HTTP_404_NOT_FOUND)

        product = Product(
            category_id=payload.category_id,
            name=payload.name.strip(),
            description=payload.description,
            price=payload.price,
            original_price=payload.original_price,
            rating=payload.rating,
            review_count=payload.review_count,
            image=payload.image,
            stock_quantity=payload.stock_quantity,
            features=payload.features,
            colors=[c.model_dump() for c in payload.colors],
            sizes=payload.sizes,
            is_best_seller=payload.is_best_seller,
            is_active=payload.is_active,
        )
        self.product_repo.add(product)
        loaded = self.product_repo.get_by_id(product.id)
        return product_to_read(loaded)  # type: ignore[arg-type]

    def update_product(self, product_id: UUID, payload: ProductUpdate) -> ProductRead:
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise AppException("Product not found.", status_code=status.HTTP_404_NOT_FOUND)

        if payload.category_id is not None:
            category = self.category_repo.get_by_id(payload.category_id)
            if not category:
                raise AppException("Category not found.", status_code=status.HTTP_404_NOT_FOUND)
            product.category_id = payload.category_id
        if payload.name is not None:
            product.name = payload.name.strip()
        if payload.description is not None:
            product.description = payload.description
        if payload.price is not None:
            product.price = payload.price
        if payload.original_price is not None:
            product.original_price = payload.original_price
        if payload.rating is not None:
            product.rating = payload.rating
        if payload.review_count is not None:
            product.review_count = payload.review_count
        if payload.image is not None:
            product.image = payload.image
        if payload.stock_quantity is not None:
            product.stock_quantity = payload.stock_quantity
        if payload.features is not None:
            product.features = payload.features
        if payload.colors is not None:
            product.colors = [c.model_dump() for c in payload.colors]
        if payload.sizes is not None:
            product.sizes = payload.sizes
        if payload.is_best_seller is not None:
            product.is_best_seller = payload.is_best_seller
        if payload.is_active is not None:
            product.is_active = payload.is_active

        self.product_repo.db.add(product)
        self.product_repo.db.commit()
        self.product_repo.db.refresh(product)
        loaded = self.product_repo.get_by_id(product.id)
        return product_to_read(loaded)  # type: ignore[arg-type]

    def delete_product(self, product_id: UUID) -> None:
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise AppException("Product not found.", status_code=status.HTTP_404_NOT_FOUND)
        self.product_repo.delete(product)
