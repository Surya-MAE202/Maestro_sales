"""Changes in user table removed check in and check out

Revision ID: dfa4ebbfcc2f
Revises: 1f9927c307a1
Create Date: 2024-10-07 09:02:56.967014

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'dfa4ebbfcc2f'
down_revision = '1f9927c307a1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'check_in')
    op.drop_column('user', 'check_out')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('check_out', mysql.DATETIME(), nullable=True))
    op.add_column('user', sa.Column('check_in', mysql.DATETIME(), nullable=True))
    # ### end Alembic commands ###
