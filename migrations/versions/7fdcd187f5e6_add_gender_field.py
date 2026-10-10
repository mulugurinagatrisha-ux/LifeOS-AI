"""Add gender field

Revision ID: 7fdcd187f5e6
Revises: d48e23785631
Create Date: 2026-10-06 18:54:15.922180
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7fdcd187f5e6"
down_revision = "d48e23785631"
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(
            sa.Column(
                "gender",
                sa.String(length=20),
                nullable=True
            )
        )


def downgrade():

    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("gender")