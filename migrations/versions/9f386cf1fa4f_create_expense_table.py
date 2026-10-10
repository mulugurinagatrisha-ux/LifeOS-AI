"""Create expense table

Revision ID: 9f386cf1fa4f
Revises: 7fdcd187f5e6
Create Date: 2026-10-06 21:39:41.032282
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9f386cf1fa4f"
down_revision = "7fdcd187f5e6"
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "expenses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(120), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("category", sa.String(50), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("created_at", sa.DateTime()),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False)
    )
def downgrade():
    op.drop_table("expenses")    