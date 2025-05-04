"""Make device_id nullable

Revision ID: 3d57c418f5f3
Revises: 9e1f132a172e
Create Date: 2025-05-03 00:38:44.466110

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3d57c418f5f3'
down_revision = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema to make device_id nullable."""
    op.alter_column('users', 'device_id',
                    existing_type=sa.String(),
                    nullable=True)


def downgrade() -> None:
    """Downgrade schema to make device_id not nullable."""
    op.alter_column('users', 'device_id',
                    existing_type=sa.String(),
                    nullable=False)