"""add mystery_moodbox_date_mapping

Revision ID: c8766bea814e
Revises: 20de7a6cc93d
Create Date: 2025-05-11 17:46:50.252426

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8766bea814e'
down_revision: Union[str, None] = '20de7a6cc93d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'mystery_moodbox_date_mapping',
        sa.Column('mapping_id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('question_id', sa.dialects.postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('scheduled_date', sa.Date(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['question_id'], ['mystery_moodbox_questions.question_id'])
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('mystery_moodbox_date_mapping')

