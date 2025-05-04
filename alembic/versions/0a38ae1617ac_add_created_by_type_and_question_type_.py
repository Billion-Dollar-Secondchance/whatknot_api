"""Add created_by_type and question_type to mystery_moodbox_questions

Revision ID: 0a38ae1617ac
Revises: 1c04785eeb40
Create Date: 2025-05-04 03:21:44.668226

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0a38ae1617ac'
down_revision: Union[str, None] = '1c04785eeb40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    created_by_type_enum = postgresql.ENUM('ADMIN', 'USER', name='createdbytype')
    created_by_type_enum.create(op.get_bind(), checkfirst=True)

    question_type_enum = postgresql.ENUM('input_text', 'single_choice', 'multi_choice', name='questiontype')
    question_type_enum.create(op.get_bind(), checkfirst=True)

    # Add with server_default temporarily for existing rows
    op.add_column(
        'mystery_moodbox_questions',
        sa.Column('created_by_type', created_by_type_enum, server_default='ADMIN', nullable=False)
    )
    op.add_column(
        'mystery_moodbox_questions',
        sa.Column('question_type', question_type_enum, server_default='input_text', nullable=False)
    )

    # Optionally drop the default after applying to existing rows
    op.alter_column('mystery_moodbox_questions', 'created_by_type', server_default=None)

def downgrade() -> None:
    op.drop_column('mystery_moodbox_questions', 'question_type')
    op.drop_column('mystery_moodbox_questions', 'created_by_type')

    # Drop enums
    question_type_enum = postgresql.ENUM('input_text', 'single_choice', 'multi_choice', name='questiontype')
    created_by_type_enum = postgresql.ENUM('ADMIN', 'USER', name='createdbytype')
    question_type_enum.drop(op.get_bind(), checkfirst=True)
    created_by_type_enum.drop(op.get_bind(), checkfirst=True)
