"""Add intrested_in to users

Revision ID: f703195a5778
Revises: e827c0d7a6b5
Create Date: 2025-05-13 11:43:05.289016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f703195a5778'
down_revision: Union[str, None] = 'e827c0d7a6b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('users', sa.Column('intrested_in', sa.String(), nullable=True))

def downgrade():
    op.drop_column('users', 'intrested_in')
