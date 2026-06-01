from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.api.deps import DbSession, get_current_user
from app.models.user import User
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.catalog import CategoryRead, ProductRead
from app.services.catalog_service import CatalogService

router = APIRouter()


def get_catalog_service(db: DbSession) -> CatalogService:
    return CatalogService(CategoryRepository(db), ProductRepository(db))


@router.get("/categories", response_model=list[CategoryRead])
def list_categories(
    _: User = Depends(get_current_user),
    service: CatalogService = Depends(get_catalog_service),
) -> list[CategoryRead]:
    return service.list_categories()


@router.get("/categories/{slug}", response_model=CategoryRead)
def get_category(
    slug: str,
    _: User = Depends(get_current_user),
    service: CatalogService = Depends(get_catalog_service),
) -> CategoryRead:
    return service.get_category_by_slug(slug)


@router.get("/products", response_model=list[ProductRead])
def list_products(
    category_slug: str | None = Query(default=None),
    best_sellers: bool = Query(default=False),
    _: User = Depends(get_current_user),
    service: CatalogService = Depends(get_catalog_service),
) -> list[ProductRead]:
    return service.list_products(category_slug=category_slug, best_sellers=best_sellers)


@router.get("/products/{product_id}", response_model=ProductRead)
def get_product(
    product_id: UUID,
    _: User = Depends(get_current_user),
    service: CatalogService = Depends(get_catalog_service),
) -> ProductRead:
    return service.get_product(product_id)
