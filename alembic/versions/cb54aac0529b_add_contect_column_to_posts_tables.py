"""add contect column to posts tables

Revision ID: cb54aac0529b
Revises: b06444c928b1
Create Date: 2022-04-23 20:47:26.387849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb54aac0529b'
down_revision = 'b06444c928b1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
