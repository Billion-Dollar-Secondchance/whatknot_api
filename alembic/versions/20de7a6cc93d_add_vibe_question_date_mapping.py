"""add vibe_question_date_mapping

Revision ID: 20de7a6cc93d
Revises: c1b14c9b9b4c
Create Date: 2025-05-11 14:44:54.820788

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '20de7a6cc93d'
down_revision: Union[str, None] = 'c1b14c9b9b4c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'vibe_question_date_mapping',
        sa.Column('mapping_id', sa.UUID(), nullable=False),
        sa.Column('question_id', sa.UUID(), nullable=False),
        sa.Column('scheduled_date', sa.Date(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['question_id'], ['vibe_questions.question_id']),
        sa.PrimaryKeyConstraint('mapping_id')
    )


def downgrade() -> None:
    op.drop_table('vibe_question_date_mapping')