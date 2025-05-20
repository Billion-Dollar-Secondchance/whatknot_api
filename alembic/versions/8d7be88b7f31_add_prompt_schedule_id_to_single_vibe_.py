"""Add prompt_schedule_id to single_vibe_prompt_response

Revision ID: 8d7be88b7f31
Revises: 0386c7db0c2a
Create Date: 2025-05-20 01:24:30.287182

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d7be88b7f31'
down_revision: Union[str, None] = '0386c7db0c2a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'single_vibe_prompt_response',
        sa.Column('prompt_schedule_id', sa.String(), sa.ForeignKey('single_vibe_prompt_schedule.prompt_schedule_id'))
    )

def downgrade() -> None:
    op.drop_column('single_vibe_prompt_response', 'prompt_schedule_id')

