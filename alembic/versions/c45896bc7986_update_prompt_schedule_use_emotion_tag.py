"""update_prompt_schedule_use_emotion_tag

Revision ID: c45896bc7986
Revises: b6675a797101
Create Date: 2025-05-14 02:10:33.182223
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c45896bc7986'
down_revision: Union[str, None] = 'b6675a797101'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Step 1: Add the column with default
    op.add_column(
        'single_vibe_prompt_schedule',
        sa.Column('emotion_tag', sa.String(), nullable=False, server_default='Unknown')
    )

    # Step 2: Drop the default after it's created (optional but clean)
    op.alter_column(
        'single_vibe_prompt_schedule',
        'emotion_tag',
        server_default=None
    )


def downgrade():
    op.drop_column('single_vibe_prompt_schedule', 'emotion_tag')
