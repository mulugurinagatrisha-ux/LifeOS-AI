"""Added Chat Sessions

Revision ID: 98c2ae9542d2
Revises: 763d23aa9346
Create Date: 2026-10-04 17:48:26.772099

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "98c2ae9542d2"
down_revision = "763d23aa9346"
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "chat_sessions",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True
        ),

        sa.Column(
            "title",
            sa.String(200),
            nullable=False
        ),

        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)")
        ),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_chat_sessions_user_id"
        )
    )

    with op.batch_alter_table("chat_history") as batch_op:

        batch_op.add_column(
            sa.Column(
                "session_id",
                sa.Integer(),
                nullable=True
            )
        )

        batch_op.create_foreign_key(
            "fk_chat_history_session_id",
            "chat_sessions",
            ["session_id"],
            ["id"]
        )


def downgrade():

    with op.batch_alter_table("chat_history") as batch_op:

        batch_op.drop_constraint(
            "fk_chat_history_session_id",
            type_="foreignkey"
        )

        batch_op.drop_column(
            "session_id"
        )

    op.drop_table("chat_sessions")