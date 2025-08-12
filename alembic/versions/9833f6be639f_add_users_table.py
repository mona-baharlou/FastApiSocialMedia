"""add Users table

Revision ID: 9833f6be639f
Revises: 3a2ad5855fc3
Create Date: 2025-08-12 15:26:17.761896

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9833f6be639f'
down_revision: Union[str, Sequence[str], None] = '3a2ad5855fc3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
               sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
               sa.Column('email', sa.String(),nullable=False,unique=True),
               sa.Column('password', sa.String(),nullable=False),
               sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
            )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
