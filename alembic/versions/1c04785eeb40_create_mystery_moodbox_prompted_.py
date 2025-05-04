"""create mystery_moodbox_prompted_questions table

Revision ID: 1c04785eeb40
Revises: c50dbb183e9f
Create Date: 2025-05-04 01:18:20.498594

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1c04785eeb40'
down_revision: Union[str, None] = 'c50dbb183e9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



# Define enum for prompt_status
promptstatus_enum = postgresql.ENUM(
    'prompted',
    'answered_by_one',
    'answered_by_both',
    'guessed',
    name='promptstatusenum',
    create_type=False  # Prevent recreation if already exists
)

def upgrade() -> None:
    promptstatus_enum.create(op.get_bind(), checkfirst=True)
    op.add_column(
        'mystery_moodbox_prompted_questions',
        sa.Column('prompt_status', promptstatus_enum, nullable=False, server_default='prompted')
    )

def downgrade() -> None:
    op.drop_column('mystery_moodbox_prompted_questions', 'prompt_status')
    promptstatus_enum.drop(op.get_bind(), checkfirst=True)