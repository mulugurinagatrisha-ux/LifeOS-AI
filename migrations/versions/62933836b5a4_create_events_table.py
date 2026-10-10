"""Create events table

Revision ID: 62933836b5a4
Revises: 98c2ae9542d2
"""

from alembic import op
import sqlalchemy as sa

revision = "62933836b5a4"
down_revision = "98c2ae9542d2"
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "events",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True
        ),

        sa.Column(
            "title",
            sa.String(length=200),
            nullable=False
        ),

        sa.Column(
            "description",
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            "event_date",
            sa.Date(),
            nullable=False
        ),

        sa.Column(
            "event_time",
            sa.Time(),
            nullable=True
        ),

        sa.Column(
            "color",
            sa.String(length=20),
            nullable=True
        ),

        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.func.now()
        ),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"]
        )

    )


def downgrade():

    op.drop_table("events")