from app.models.product import Product
from app.schemas.catalog import CategoryRead, ProductColorRead, ProductRead


def product_to_read(product: Product) -> ProductRead:
    colors = [
        ProductColorRead.model_validate(c) if isinstance(c, dict) else c
        for c in (product.colors or [])
    ]
    images = list(product.images or [])
    if not images and product.image:
        images = [product.image]
    return ProductRead(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        original_price=product.original_price,
        rating=product.rating,
        review_count=product.review_count,
        image=product.image,
        images=images,
        stock_quantity=product.stock_quantity,
        features=list(product.features or []),
        colors=colors,
        sizes=list(product.sizes or []),
        is_best_seller=product.is_best_seller,
        category_id=product.category_id,
        category_slug=product.category.slug if product.category else "",
        is_active=product.is_active,
    )


def category_to_read(category, item_count: int) -> CategoryRead:
    return CategoryRead(
        id=category.id,
        slug=category.slug,
        name=category.name,
        image=category.image,
        bg_color=category.bg_color,
        item_count=item_count,
    )
