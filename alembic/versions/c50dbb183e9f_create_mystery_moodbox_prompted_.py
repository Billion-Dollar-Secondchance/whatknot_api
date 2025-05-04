"""create mystery_moodbox_prompted_questions table

Revision ID: c50dbb183e9f
Revises: a9788e9e32b6
Create Date: 2025-05-04 01:01:31.819680

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers, used by Alembic.
revision: str = 'c50dbb183e9f'
down_revision: Union[str, None] = 'a9788e9e32b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'mystery_moodbox_prompted_questions',
        sa.Column('prompt_id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('pair_id', sa.String(), sa.ForeignKey('partner_pairing.pair_id', ondelete='CASCADE'), nullable=False),
        sa.Column('question_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('mystery_moodbox_questions.question_id', ondelete='CASCADE'), nullable=False),
        sa.Column('prompted_user_id', sa.String(), sa.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False)
    )

def downgrade():
    op.drop_table('mystery_moodbox_prompted_questions')