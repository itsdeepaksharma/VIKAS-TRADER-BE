"""Add selected color and size to order items."""

from alembic import op
import sqlalchemy as sa

revision = "0007_order_item_variants"
down_revision = "0006_user_avatar_url"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "order_items",
        sa.Column("selected_color", sa.String(length=100), nullable=True),
    )
    op.add_column(
        "order_items",
        sa.Column("selected_size", sa.String(length=100), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("order_items", "selected_size")
    op.drop_column("order_items", "selected_color")
