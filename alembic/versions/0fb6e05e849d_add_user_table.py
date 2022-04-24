"""add user table

Revision ID: 0fb6e05e849d
Revises: cb54aac0529b
Create Date: 2022-04-23 21:11:50.471374

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fb6e05e849d'
down_revision = 'cb54aac0529b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('userss',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    pass


def downgrade():
    op.drop_table('userss')
    pass
