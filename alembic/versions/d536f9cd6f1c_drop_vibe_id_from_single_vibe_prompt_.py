"""drop vibe_id from single_vibe_prompt_schedule

Revision ID: d536f9cd6f1c
Revises: c45896bc7986
Create Date: 2025-05-14 02:41:46.342794

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd536f9cd6f1c'
down_revision: Union[str, None] = 'c45896bc7986'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_column('single_vibe_prompt_schedule', 'vibe_id')

def downgrade():
    from sqlalchemy import Column, String
    op.add_column('single_vibe_prompt_schedule', Column('vibe_id', String, nullable=False))