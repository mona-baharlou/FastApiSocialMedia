"""Create posts table

Revision ID: 3a2ad5855fc3
Revises: 
Create Date: 2025-08-12 14:54:42.838269

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a2ad5855fc3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
               sa.Column('title', sa.String(),nullable=False),
               sa.Column('content', sa.String(),nullable=False),
               sa.Column('published', sa.Boolean, nullable=False, server_default=sa.text('true')),
               sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
            )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass
