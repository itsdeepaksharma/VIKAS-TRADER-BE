from decimal import Decimal

import structlog
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.product import Product
from app.repositories.category_repository import CategoryRepository

logger = structlog.get_logger(__name__)

CATEGORIES = [
    {
        "slug": "buckets-mugs",
        "name": "Buckets & Mugs",
        "image": "https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=400&h=400&fit=crop",
        "bg_color": "bg-vt-light-blue",
        "sort_order": 1,
    },
    {
        "slug": "baskets-organizers",
        "name": "Baskets & Organizers",
        "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop",
        "bg_color": "bg-vt-light-mint",
        "sort_order": 2,
    },
    {
        "slug": "containers",
        "name": "Containers",
        "image": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop",
        "bg_color": "bg-amber-50",
        "sort_order": 3,
    },
    {
        "slug": "kitchenware",
        "name": "Kitchenware",
        "image": "https://images.unsplash.com/photo-1556909202-7a9a0f8b0f0f?w=400&h=400&fit=crop",
        "bg_color": "bg-orange-50",
        "sort_order": 4,
    },
    {
        "slug": "cleaning-supplies",
        "name": "Cleaning Supplies",
        "image": "https://images.unsplash.com/photo-1563453392213-326a0a0c0f0f?w=400&h=400&fit=crop",
        "bg_color": "bg-sky-50",
        "sort_order": 5,
    },
    {
        "slug": "household",
        "name": "Household",
        "image": "https://images.unsplash.com/photo-1585421514288-efb74c2b69bb?w=400&h=400&fit=crop",
        "bg_color": "bg-vt-light-blue",
        "sort_order": 6,
    },
    {
        "slug": "storage",
        "name": "Storage Solutions",
        "image": "https://images.unsplash.com/photo-1595428774223-ef9bbecbb547?w=400&h=400&fit=crop",
        "bg_color": "bg-vt-light-mint",
        "sort_order": 7,
    },
    {
        "slug": "wholesale",
        "name": "Wholesale Packs",
        "image": "https://images.unsplash.com/photo-1604719312566-8912e9227c6a?w=400&h=400&fit=crop",
        "bg_color": "bg-emerald-50",
        "sort_order": 8,
    },
]

BASE_COLORS = [
    {"id": "blue", "name": "Blue", "hex": "#00A3FF"},
    {"id": "green", "name": "Green", "hex": "#39FF6A"},
    {"id": "white", "name": "White", "hex": "#FFFFFF"},
]
BASE_FEATURES = ["BPA Free", "Food Grade", "Air Tight", "Durable"]


def ensure_catalog_seed(db: Session) -> None:
    repo = CategoryRepository(db)
    if repo.list_all():
        return

    slug_to_id: dict[str, object] = {}
    for idx, data in enumerate(CATEGORIES):
        category = Category(**data, is_active=True)
        db.add(category)
        db.flush()
        slug_to_id[data["slug"]] = category.id

    products = [
        {
            "slug": "containers",
            "name": "Milton Storage Container Set (5 Pcs)",
            "price": Decimal("899"),
            "original_price": Decimal("1199"),
            "rating": Decimal("4.7"),
            "review_count": 234,
            "image": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&h=600&fit=crop",
            "stock_quantity": 50,
            "is_best_seller": True,
            "sizes": ["1.5 L", "2.5 L", "5 L"],
        },
        {
            "slug": "buckets-mugs",
            "name": "Heavy Duty Plastic Bucket 20L",
            "price": Decimal("349"),
            "original_price": Decimal("449"),
            "rating": Decimal("4.5"),
            "review_count": 189,
            "image": "https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=600&h=600&fit=crop",
            "stock_quantity": 30,
            "is_best_seller": True,
            "sizes": ["15 L", "20 L", "25 L"],
            "colors": [
                {"id": "blue", "name": "Blue", "hex": "#00A3FF"},
                {"id": "red", "name": "Red", "hex": "#EF4444"},
            ],
            "features": ["Durable", "Leak Proof", "Easy Grip Handle"],
        },
        {
            "slug": "baskets-organizers",
            "name": "Multi-Purpose Storage Basket",
            "price": Decimal("299"),
            "rating": Decimal("4.6"),
            "review_count": 156,
            "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=600&fit=crop",
            "stock_quantity": 40,
            "is_best_seller": True,
            "sizes": ["Small", "Medium", "Large"],
        },
        {
            "slug": "kitchenware",
            "name": "Kitchen Lunch Box Set (3 Tier)",
            "price": Decimal("549"),
            "original_price": Decimal("699"),
            "rating": Decimal("4.8"),
            "review_count": 312,
            "image": "https://images.unsplash.com/photo-1556909202-7a9a0f8b0f0f?w=600&h=600&fit=crop",
            "stock_quantity": 25,
            "is_best_seller": True,
            "sizes": ["750 ml", "1 L", "1.5 L"],
        },
        {
            "slug": "containers",
            "name": "Airtight Food Jar 1.2L",
            "price": Decimal("199"),
            "rating": Decimal("4.4"),
            "review_count": 98,
            "image": "https://images.unsplash.com/photo-1595428774223-ef9bbecbb547?w=600&h=600&fit=crop",
            "stock_quantity": 60,
            "sizes": ["800 ml", "1.2 L", "2 L"],
        },
        {
            "slug": "cleaning-supplies",
            "name": "Floor Cleaning Mop Bucket",
            "price": Decimal("449"),
            "rating": Decimal("4.3"),
            "review_count": 87,
            "image": "https://images.unsplash.com/photo-1563453392213-326a0a0c0f0f?w=600&h=600&fit=crop",
            "stock_quantity": 0,
            "sizes": ["12 L", "16 L"],
            "colors": [{"id": "blue", "name": "Blue", "hex": "#00A3FF"}],
            "features": ["Wheels", "Wringer", "Durable"],
        },
        {
            "slug": "storage",
            "name": "Stackable Drawer Organizer",
            "price": Decimal("399"),
            "rating": Decimal("4.6"),
            "review_count": 145,
            "image": "https://images.unsplash.com/photo-1585421514288-efb74c2b69bb?w=600&h=600&fit=crop",
            "stock_quantity": 20,
            "sizes": ["S", "M", "L"],
            "features": ["Modular", "Transparent", "Stackable"],
        },
        {
            "slug": "wholesale",
            "name": "Wholesale Plastic Mug Pack (48 Pcs)",
            "price": Decimal("1299"),
            "original_price": Decimal("1599"),
            "rating": Decimal("4.9"),
            "review_count": 56,
            "image": "https://images.unsplash.com/photo-1604719312566-8912e9227c6a?w=600&h=600&fit=crop",
            "stock_quantity": 15,
            "sizes": ["250 ml"],
            "colors": [{"id": "white", "name": "White", "hex": "#FFFFFF"}],
            "features": ["Bulk Pack", "Restaurant Grade", "BPA Free"],
        },
    ]

    for item in products:
        db.add(
            Product(
                category_id=slug_to_id[item["slug"]],
                name=item["name"],
                description=item.get("description", f"Quality {item['name']} from Vikas Traders."),
                price=item["price"],
                original_price=item.get("original_price"),
                rating=item["rating"],
                review_count=item["review_count"],
                image=item["image"],
                stock_quantity=item["stock_quantity"],
                features=item.get("features", BASE_FEATURES),
                colors=item.get("colors", BASE_COLORS),
                sizes=item.get("sizes", []),
                is_best_seller=item.get("is_best_seller", False),
                is_active=True,
            )
        )

    db.commit()
    logger.info("catalog_seed_created", categories=len(CATEGORIES), products=len(products))
