from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'a9788e9e32b6'
down_revision = '3d57c418f5f3'
branch_labels = None
depends_on = None

createdby_enum = postgresql.ENUM('admin', 'user', name='createdbytype')
questiontype_enum = postgresql.ENUM('input_text', 'single_choice', 'multi_choice', name='questiontype')

def upgrade():
    op.create_table(
        'mystery_moodbox_questions',
        sa.Column('question_id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('pair_id', sa.String(), sa.ForeignKey('partner_pairing.pair_id', ondelete='CASCADE'), nullable=True),
        sa.Column('created_by_type', createdby_enum, nullable=False),
        sa.Column('submitted_by', sa.String(), nullable=True),
        sa.Column('question_type', questiontype_enum, nullable=False, server_default='input_text'),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('options', postgresql.JSONB, nullable=True),
        sa.Column('correct_answer', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
    )

def downgrade():
    op.drop_table('mystery_moodbox_questions')
    questiontype_enum.drop(op.get_bind(), checkfirst=True)
    createdby_enum.drop(op.get_bind(), checkfirst=True)
