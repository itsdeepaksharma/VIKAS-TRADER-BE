"""Expand image columns for uploaded data URLs."""

from alembic import op
import sqlalchemy as sa

revision = "0004_expand_image_columns"
down_revision = "0003_catalog_and_orders"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "categories",
        "image",
        existing_type=sa.String(length=500),
        type_=sa.Text(),
        existing_nullable=False,
    )
    op.alter_column(
        "products",
        "image",
        existing_type=sa.String(length=500),
        type_=sa.Text(),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "categories",
        "image",
        existing_type=sa.Text(),
        type_=sa.String(length=500),
        existing_nullable=False,
    )
    op.alter_column(
        "products",
        "image",
        existing_type=sa.Text(),
        type_=sa.String(length=500),
        existing_nullable=False,
    )
