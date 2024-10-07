"""changes in api_token tables

Revision ID: 3dec01a17aaf
Revises: b363fa74f4d7
Create Date: 2024-10-05 14:04:21.148403

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3dec01a17aaf'
down_revision = 'b363fa74f4d7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('check_out', sa.DateTime(), nullable=True))
    op.drop_column('user', 'check_outs')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('check_outs', mysql.DATETIME(), nullable=True))
    op.drop_column('user', 'check_out')
    # ### end Alembic commands ###
