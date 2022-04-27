"""votes

Revision ID: 8b33ddfd9f15
Revises: fa4ba885b6d3
Create Date: 2022-04-27 21:35:22.621894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b33ddfd9f15'
down_revision = 'fa4ba885b6d3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('votes')
    op.add_column('votes', sa.Column('post_id', sa.Integer(), nullable=False))
    op.add_column('votes', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('votes_post_id_fkey', source_table='votes', referent_table='postssd', local_cols=['post_id'], remote_cols=['id'], ondelete='CASCADE')
    op.create_foreign_key('votes_user_id_fkey', source_table='votes', referent_table='userss', local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE')
    
    pass


def downgrade():
    op.drop_constraint('votes_post_id_fkey', table_name='votes')
    op.drop_constraint('votes_user_id_fkey', table_name='votes')
    op.drop_table('votes')
    pass
