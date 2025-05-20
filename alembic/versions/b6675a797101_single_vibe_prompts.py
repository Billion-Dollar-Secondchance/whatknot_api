"""single_vibe_prompts

Revision ID: b6675a797101
Revises: 60c388ffda0d
Create Date: 2025-05-14 01:40:02.848243

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6675a797101'
down_revision: Union[str, None] = '60c388ffda0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('single_vibe_prompts', sa.Column('prompt_type', sa.String(), nullable=False, server_default='emotion_checkin'))
    op.add_column('single_vibe_prompts', sa.Column('emotion_tag', sa.String(), nullable=True))
    op.add_column('single_vibe_prompts', sa.Column('options', sa.Text(), nullable=True))
    op.add_column('single_vibe_prompts', sa.Column('allow_other', sa.String(), nullable=True))

def downgrade():
    op.drop_column('single_vibe_prompts', 'prompt_type')
    op.drop_column('single_vibe_prompts', 'emotion_tag')
    op.drop_column('single_vibe_prompts', 'options')
    op.drop_column('single_vibe_prompts', 'allow_other')