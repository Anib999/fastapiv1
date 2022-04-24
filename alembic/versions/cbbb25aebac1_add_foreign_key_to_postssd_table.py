"""Add foreign key to postssd table

Revision ID: cbbb25aebac1
Revises: 0fb6e05e849d
Create Date: 2022-04-23 21:17:38.271973

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbbb25aebac1'
down_revision = '0fb6e05e849d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('postssd', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='postssd', referent_table='userss', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name='postssd')
    op.drop_column('postssd', 'owner_id')
    pass
