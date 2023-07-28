"""Add brand to credit cards table

Revision ID: cd6d9d864e2c
Revises: 4aafc68524a4
Create Date: 2023-07-17 18:06:48.636864

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "cd6d9d864e2c"
down_revision = "4aafc68524a4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("credit_cards", sa.Column("brand", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("credit_cards", "brand")
