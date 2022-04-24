"""all leftovers in postssd

Revision ID: 38eab75621a2
Revises: cbbb25aebac1
Create Date: 2022-04-23 21:23:20.510021

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38eab75621a2'
down_revision = 'cbbb25aebac1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('postssd', sa.Column('published', sa.Boolean(), nullable=False, server_default="TRUE"),)
    op.add_column('postssd', sa.Column('created_at', sa.TIMESTAMP(timezone=True ), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('postssd', 'published')
    op.drop_column('postssd', 'created_at')
    pass
