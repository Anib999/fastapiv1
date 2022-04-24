"""data changes

Revision ID: b06444c928b1
Revises: 
Create Date: 2022-04-21 21:16:47.158460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b06444c928b1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('postssd', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('postssd')
    pass
