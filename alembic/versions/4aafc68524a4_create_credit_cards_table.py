"""create credit cards table

Revision ID: 4aafc68524a4
Revises: 
Create Date: 2023-07-15 19:55:02.906941

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "4aafc68524a4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "credit_cards",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("exp_date", sa.Date(), nullable=True),
        sa.Column("holder", sa.String(), nullable=True),
        sa.Column("number", sa.String(), nullable=True),
        sa.Column("cvv", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("credit_cards")
