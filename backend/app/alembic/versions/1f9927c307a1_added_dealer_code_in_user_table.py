"""Added dealer_code in user table

Revision ID: 1f9927c307a1
Revises: 101d0337c67b
Create Date: 2024-10-05 17:18:27.027024

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f9927c307a1'
down_revision = '101d0337c67b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('dealer_code', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'dealer_code')
    # ### end Alembic commands ###
