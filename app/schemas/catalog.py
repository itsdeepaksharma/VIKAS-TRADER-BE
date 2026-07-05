from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator


class ProductColorRead(BaseModel):
    id: str
    name: str
    hex: str


class CategoryRead(BaseModel):
    id: UUID
    slug: str
    name: str
    image: str
    bg_color: str
    item_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class ProductRead(BaseModel):
    id: UUID
    name: str
    description: str
    price: Decimal
    original_price: Decimal | None
    rating: Decimal
    review_count: int
    image: str
    images: list[str] = Field(default_factory=list)
    stock_quantity: int
    features: list[str]
    colors: list[ProductColorRead]
    sizes: list[str]
    is_best_seller: bool
    category_id: UUID
    category_slug: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def in_stock(self) -> bool:
        return self.stock_quantity > 0


class CategoryCreate(BaseModel):
    slug: str | None = Field(default=None, min_length=2, max_length=120)
    name: str = Field(min_length=2, max_length=200)
    image: str | None = Field(default=None, max_length=1_000_000)
    bg_color: str = Field(default="bg-vt-light-blue", max_length=50)
    sort_order: int = 0
    is_active: bool = True


class CategoryUpdate(BaseModel):
    slug: str | None = Field(default=None, min_length=2, max_length=120)
    name: str | None = Field(default=None, min_length=2, max_length=200)
    image: str | None = Field(default=None, max_length=1_000_000)
    bg_color: str | None = Field(default=None, max_length=50)
    sort_order: int | None = None
    is_active: bool | None = None


class ProductCreate(BaseModel):
    category_id: UUID
    name: str = Field(min_length=2, max_length=300)
    description: str = ""
    price: Decimal = Field(gt=0)
    original_price: Decimal | None = Field(default=None, gt=0)
    rating: Decimal = Field(default=Decimal("4.5"), ge=0, le=5)
    review_count: int = Field(default=0, ge=0)
    image: str | None = Field(default=None, max_length=1_000_000)
    images: list[str] = Field(default_factory=list, max_length=10)
    stock_quantity: int = Field(default=0, ge=0)
    features: list[str] = Field(default_factory=list)
    colors: list[ProductColorRead] = Field(default_factory=list)
    sizes: list[str] = Field(default_factory=list)
    is_best_seller: bool = False
    is_active: bool = True

    @model_validator(mode="after")
    def validate_images(self) -> "ProductCreate":
        cleaned = [url.strip() for url in self.images if url and url.strip()]
        if cleaned:
            self.images = cleaned
            if not self.image:
                self.image = cleaned[0]
            return self
        if self.image and len(self.image.strip()) >= 5:
            self.images = [self.image.strip()]
            return self
        raise ValueError("At least one product image is required.")


class ProductUpdate(BaseModel):
    category_id: UUID | None = None
    name: str | None = Field(default=None, min_length=2, max_length=300)
    description: str | None = None
    price: Decimal | None = Field(default=None, gt=0)
    original_price: Decimal | None = None
    rating: Decimal | None = Field(default=None, ge=0, le=5)
    review_count: int | None = Field(default=None, ge=0)
    image: str | None = Field(default=None, max_length=1_000_000)
    images: list[str] | None = Field(default=None, max_length=10)
    stock_quantity: int | None = Field(default=None, ge=0)
    features: list[str] | None = None
    colors: list[ProductColorRead] | None = None
    sizes: list[str] | None = None
    is_best_seller: bool | None = None
    is_active: bool | None = None
