"""add user profile fields

Revision ID: 0002_add_user_profile_fields
Revises: 0001_create_users
Create Date: 2026-05-30 00:00:00.000000
"""

import sqlalchemy as sa
from alembic import op

revision = "0002_add_user_profile_fields"
down_revision = "0001_create_users"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("first_name", sa.String(length=100), nullable=False, server_default="User"),
    )
    op.add_column(
        "users",
        sa.Column("last_name", sa.String(length=100), nullable=False, server_default="Account"),
    )
    op.add_column(
        "users",
        sa.Column("phone", sa.String(length=20), nullable=False, server_default="0000000000"),
    )
    op.add_column(
        "users",
        sa.Column("address", sa.Text(), nullable=False, server_default="Not provided"),
    )
    op.alter_column("users", "first_name", server_default=None)
    op.alter_column("users", "last_name", server_default=None)
    op.alter_column("users", "phone", server_default=None)
    op.alter_column("users", "address", server_default=None)
    op.create_index(op.f("ix_users_phone"), "users", ["phone"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_users_phone"), table_name="users")
    op.drop_column("users", "address")
    op.drop_column("users", "phone")
    op.drop_column("users", "last_name")
    op.drop_column("users", "first_name")
