"""single_vibe_entries

Revision ID: 1db538aef29f
Revises: 02b170ce9218
Create Date: 2025-05-13 12:26:15.455830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1db538aef29f'
down_revision: Union[str, None] = '02b170ce9218'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'single_vibe_entries',
        sa.Column('single_vibe_id', sa.String(), primary_key=True, index=True),
        sa.Column('user_id', sa.String(), nullable=False, index=True),
        sa.Column('vibe', sa.String(), nullable=False),
        sa.Column('prompt_answers', sa.Text(), nullable=True),
        sa.Column('answer_status', sa.String(), nullable=False, server_default='incomplete'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )

def downgrade():
    op.drop_table('single_vibe_entries')