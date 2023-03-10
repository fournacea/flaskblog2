"""added profile_pic, corrected VARCHAR requires length error

Revision ID: a61e6b4ba8e1
Revises: 5efed8eeba01
Create Date: 2023-02-13 10:54:26.451543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a61e6b4ba8e1'
down_revision = '5efed8eeba01'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_pic', sa.String(length=300), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('profile_pic')

    # ### end Alembic commands ###
