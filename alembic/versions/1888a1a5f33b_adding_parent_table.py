"""Adding Parent table

Revision ID: 1888a1a5f33b
Revises: e3c8cc9a66fd
Create Date: 2024-02-09 21:49:43.084969

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '1888a1a5f33b'
down_revision: Union[str, None] = 'e3c8cc9a66fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Parent',
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('email_id', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['student_id'], ['Student.student_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('parent_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Parent')
    # ### end Alembic commands ###
