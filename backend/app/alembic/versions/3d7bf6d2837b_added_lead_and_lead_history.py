"""Added lead and lead_history

Revision ID: 3d7bf6d2837b
Revises: 56c23093316e
Create Date: 2024-10-08 16:50:56.740151

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3d7bf6d2837b'
down_revision = '56c23093316e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lead',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_followup', mysql.TINYINT(), nullable=True, comment='1->active,2-completed,-1->inactive'),
    sa.Column('name', sa.String(length=250), nullable=True),
    sa.Column('remarks', sa.Text(), nullable=True),
    sa.Column('company_name', sa.String(length=250), nullable=True),
    sa.Column('contact_person', sa.String(length=250), nullable=True),
    sa.Column('lead_code', sa.String(length=200), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('alternative_no', sa.String(length=20), nullable=True),
    sa.Column('landline_number', sa.String(length=20), nullable=True),
    sa.Column('whatsapp_no', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('address', sa.Text(), nullable=True),
    sa.Column('area', sa.String(length=200), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('enquiry_type_id', sa.Integer(), nullable=True),
    sa.Column('lead_status_id', sa.Integer(), nullable=True),
    sa.Column('requirements_id', sa.Integer(), nullable=True),
    sa.Column('refer_country_code', sa.String(length=10), nullable=True),
    sa.Column('approximate_amount', sa.String(length=50), nullable=True),
    sa.Column('country', sa.String(length=50), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('states', sa.String(length=50), nullable=True),
    sa.Column('pincode', sa.String(length=10), nullable=True),
    sa.Column('dealer_id', sa.Integer(), nullable=True),
    sa.Column('assigned_to', sa.Integer(), nullable=True),
    sa.Column('deletedBy', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('received_at', sa.DateTime(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('is_valid', mysql.TINYINT(), nullable=True, comment='1->valid,2->invalid'),
    sa.Column('refered_by', sa.String(length=200), nullable=True),
    sa.Column('is_active', mysql.TINYINT(), nullable=True, comment='1->active,0->inactive'),
    sa.Column('notes', sa.String(length=200), nullable=True),
    sa.Column('comments_description', sa.Text(), nullable=True),
    sa.Column('created_t', sa.DateTime(), nullable=True),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.Column('status', mysql.TINYINT(), nullable=True, comment='1->active,-1->deleted,0->inactive'),
    sa.Column('is_transferred', mysql.TINYINT(), nullable=True, comment='1->yes,0->No'),
    sa.Column('tempComment', sa.Text(), nullable=True),
    sa.Column('schedule_date', sa.DateTime(), nullable=True),
    sa.Column('poc_date', sa.DateTime(), nullable=True),
    sa.Column('demo_date', sa.DateTime(), nullable=True),
    sa.Column('transferComment', sa.Text(), nullable=True),
    sa.Column('refered_ph_no', sa.String(length=20), nullable=True),
    sa.Column('drop_reason', sa.Text(), nullable=True),
    sa.Column('latitude', sa.String(length=255), nullable=True),
    sa.Column('longitude', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['assigned_to'], ['user.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['customer_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['dealer_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['deletedBy'], ['user.id'], ),
    sa.ForeignKeyConstraint(['enquiry_type_id'], ['enquiry_type.id'], ),
    sa.ForeignKeyConstraint(['lead_status_id'], ['lead_status.id'], ),
    sa.ForeignKeyConstraint(['requirements_id'], ['requirements.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lead_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lead_id', sa.Integer(), nullable=True),
    sa.Column('leadStatus', sa.String(length=200), nullable=True),
    sa.Column('lead_status_id', sa.Integer(), nullable=True),
    sa.Column('enquiry_type_id', sa.Integer(), nullable=True),
    sa.Column('changedBy', sa.Integer(), nullable=True),
    sa.Column('longitude', sa.String(length=200), nullable=True),
    sa.Column('latitude', sa.String(length=200), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('status', mysql.TINYINT(), nullable=True, comment=' 1->active,-1->deleted'),
    sa.ForeignKeyConstraint(['changedBy'], ['user.id'], ),
    sa.ForeignKeyConstraint(['enquiry_type_id'], ['enquiry_type.id'], ),
    sa.ForeignKeyConstraint(['lead_id'], ['lead.id'], ),
    sa.ForeignKeyConstraint(['lead_status_id'], ['lead_status.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lead_history')
    op.drop_table('lead')
    # ### end Alembic commands ###
