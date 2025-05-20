"""Update the flag name to users

Revision ID: 02b170ce9218
Revises: f703195a5778
Create Date: 2025-05-13 12:05:40.730795

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '02b170ce9218'
down_revision: Union[str, None] = 'f703195a5778'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column('users', 'intrested_in', new_column_name='interested_in')

def downgrade():
    op.alter_column('users', 'interested_in', new_column_name='intrested_in')
