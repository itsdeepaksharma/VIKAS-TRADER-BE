"""Add user avatar_url column."""

from alembic import op
import sqlalchemy as sa

revision = "0006_user_avatar_url"
down_revision = "0005_product_images"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("avatar_url", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "avatar_url")
