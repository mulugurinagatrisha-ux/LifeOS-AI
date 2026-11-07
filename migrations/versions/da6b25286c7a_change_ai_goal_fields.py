"""change ai goal fields

Revision ID: da6b25286c7a
Revises: c92ce037f522
Create Date: 2026-11-07 15:30:33.605101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da6b25286c7a'
down_revision = 'c92ce037f522'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('ai_goals', schema=None) as batch_op:
        batch_op.alter_column(
            'current_value',
            existing_type=sa.INTEGER(),
            type_=sa.String(length=100),
            existing_nullable=True
        )

        batch_op.alter_column(
            'target_value',
            existing_type=sa.INTEGER(),
            type_=sa.String(length=100),
            existing_nullable=True
        )

def downgrade():
    with op.batch_alter_table('ai_goals', schema=None) as batch_op:
        batch_op.alter_column(
            'target_value',
            existing_type=sa.String(length=100),
            type_=sa.INTEGER(),
            existing_nullable=True
        )

        batch_op.alter_column(
            'current_value',
            existing_type=sa.String(length=100),
            type_=sa.INTEGER(),
            existing_nullable=True
        )
