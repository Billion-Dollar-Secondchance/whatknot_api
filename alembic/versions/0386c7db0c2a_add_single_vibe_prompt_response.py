"""Add single_vibe_prompt_response

Revision ID: 0386c7db0c2a
Revises: d536f9cd6f1c
Create Date: 2025-05-20 01:02:55.684075

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0386c7db0c2a'
down_revision: Union[str, None] = 'd536f9cd6f1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # In your migration upgrade() function
    op.create_table(
    'single_vibe_prompt_response',
    sa.Column('response_id', sa.String(), primary_key=True, nullable=False),
    sa.Column('prompt_id', sa.String(), nullable=False),  # <-- temporarily without FK
    sa.Column('user_id', sa.String(), sa.ForeignKey('users.user_id'), nullable=False),
    sa.Column('answer', sa.String(), nullable=False),
    sa.Column('submitted_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
)



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('single_vibe_prompt_response')

