"""Add product images JSONB column."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = "0005_product_images"
down_revision = "0004_expand_image_columns"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "products",
        sa.Column("images", JSONB, server_default=sa.text("'[]'::jsonb"), nullable=False),
    )
    op.execute(
        "UPDATE products SET images = jsonb_build_array(image) WHERE jsonb_array_length(images) = 0"
    )


def downgrade() -> None:
    op.drop_column("products", "images")
