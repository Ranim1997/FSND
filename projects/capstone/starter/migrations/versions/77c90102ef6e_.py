"""empty message

Revision ID: 77c90102ef6e
Revises: 
Create Date: 2020-12-24 14:06:41.316423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77c90102ef6e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Performance', 'movie_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Performance', 'movie_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
