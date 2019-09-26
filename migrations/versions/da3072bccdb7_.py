"""empty message

Revision ID: da3072bccdb7
Revises: 7435b0a865e6
Create Date: 2019-09-26 09:58:29.485846

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da3072bccdb7'
down_revision = '7435b0a865e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project_favorites',
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.alter_column('users', 'expert_mode',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text('false'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'expert_mode',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text('false'))
    op.drop_table('project_favorites')
    # ### end Alembic commands ###
