"""Add profile fields

Revision ID: d48e23785631
Revises: 7b5e9daa4d32
Create Date: 2026-10-06 15:54:05.936544

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d48e23785631"
down_revision = "7b5e9daa4d32"
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(
            sa.Column("phone", sa.String(length=20), nullable=True)
        )

        batch_op.add_column(
            sa.Column("bio", sa.Text(), nullable=True)
        )

        batch_op.add_column(
            sa.Column(
                "profile_image",
                sa.String(length=255),
                nullable=True,
                server_default="default.png"
            )
        )


def downgrade():

    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("profile_image")
        batch_op.drop_column("bio")
        batch_op.drop_column("phone")