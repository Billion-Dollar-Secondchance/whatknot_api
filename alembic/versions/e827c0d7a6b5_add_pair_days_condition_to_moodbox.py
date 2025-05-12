"""“add_pair_days_condition_to_moodbox”

Revision ID: e827c0d7a6b5
Revises: c8766bea814e
Create Date: 2025-05-11 23:54:21.594543

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e827c0d7a6b5'
down_revision: Union[str, None] = 'c8766bea814e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'mystery_moodbox_date_mapping',
        sa.Column('pair_days_condition', sa.String(), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('mystery_moodbox_date_mapping', 'pair_days_condition')