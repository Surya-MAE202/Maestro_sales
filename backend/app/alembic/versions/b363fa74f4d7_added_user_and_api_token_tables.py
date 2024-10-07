"""added user and api_token tables

Revision ID: b363fa74f4d7
Revises: 8ddba43b1326
Create Date: 2024-10-05 14:03:31.577337

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b363fa74f4d7'
down_revision = '8ddba43b1326'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone_country_code', sa.String(length=10), nullable=True),
    sa.Column('whatsapp_country_code', sa.String(length=10), nullable=True),
    sa.Column('alter_country_code', sa.String(length=10), nullable=True),
    sa.Column('user_type', mysql.TINYINT(), nullable=True, comment='1->superAdmin,2->Admin,3->dealer,3->dealerAdmin,4->Employee,5->Customer'),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('landline_number', sa.String(length=20), nullable=True),
    sa.Column('alternative_number', sa.String(length=20), nullable=True),
    sa.Column('whatsapp_no', sa.String(length=20), nullable=True),
    sa.Column('company_name', sa.String(length=250), nullable=True),
    sa.Column('address', sa.Text(), nullable=True),
    sa.Column('area', sa.String(length=150), nullable=True),
    sa.Column('country', sa.String(length=50), nullable=True),
    sa.Column('states', sa.String(length=50), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('pincode', sa.String(length=10), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('dealer_id', sa.Integer(), nullable=True),
    sa.Column('is_active', mysql.TINYINT(), nullable=True, comment='1->active,0->inactive'),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.Column('reset_key', sa.String(length=255), nullable=True),
    sa.Column('otp', sa.String(length=10), nullable=True),
    sa.Column('otp_expire_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('check_in', sa.DateTime(), nullable=True),
    sa.Column('check_outs', sa.DateTime(), nullable=True),
    sa.Column('status', mysql.TINYINT(), nullable=True, comment='-1->delete,1->active,0->inactive'),
    sa.ForeignKeyConstraint(['dealer_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('api_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('token', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('renewed_at', sa.DateTime(), nullable=True),
    sa.Column('device_type', mysql.TINYINT(display_width=1), nullable=True, comment='1-Android, 2-iOS'),
    sa.Column('validity', mysql.TINYINT(display_width=1), nullable=True, comment='0-Expired, 1- Lifetime'),
    sa.Column('device_id', sa.String(length=255), nullable=True),
    sa.Column('device_ip', sa.String(length=255), nullable=True),
    sa.Column('status', mysql.TINYINT(display_width=1), nullable=True, comment='1-active, -1 inactive, 0- deleted'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('api_tokens')
    op.drop_table('user')
    # ### end Alembic commands ###
