"""create_single_vibe_related_tables

Revision ID: 60c388ffda0d
Revises: 1db538aef29f
Create Date: 2025-05-13 13:40:14.043438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60c388ffda0d'
down_revision: Union[str, None] = '1db538aef29f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'single_vibe_definitions',
        sa.Column('vibe_id', sa.String(), primary_key=True, index=True),
        sa.Column('name', sa.String(), unique=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    op.create_table(
        'single_vibe_schedule',
        sa.Column('schedule_id', sa.String(), primary_key=True, index=True),
        sa.Column('vibe_id', sa.String(), sa.ForeignKey('single_vibe_definitions.vibe_id'), nullable=False),
        sa.Column('scheduled_date', sa.Date(), nullable=False)
    )
    op.create_table(
        'single_vibe_prompts',
        sa.Column('prompt_id', sa.String(), primary_key=True, index=True),
        sa.Column('prompt_text', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    op.create_table(
        'single_vibe_prompt_schedule',
        sa.Column('prompt_schedule_id', sa.String(), primary_key=True, index=True),
        sa.Column('prompt_id', sa.String(), sa.ForeignKey('single_vibe_prompts.prompt_id'), nullable=False),
        sa.Column('vibe_id', sa.String(), sa.ForeignKey('single_vibe_definitions.vibe_id'), nullable=False),
        sa.Column('scheduled_date', sa.Date(), nullable=False)
    )

def downgrade():
    op.drop_table('single_vibe_prompt_schedule')
    op.drop_table('single_vibe_prompts')
    op.drop_table('single_vibe_schedule')
    op.drop_table('single_vibe_definitions')
