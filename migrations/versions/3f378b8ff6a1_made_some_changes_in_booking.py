"""made some changes in booking

Revision ID: 3f378b8ff6a1
Revises: 2e5d5070463f
Create Date: 2025-06-29 23:40:53.898919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f378b8ff6a1'
down_revision = '2e5d5070463f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.add_column(sa.Column('start_time', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('end_time', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('parking_date', sa.Date(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.drop_column('parking_date')
        batch_op.drop_column('end_time')
        batch_op.drop_column('start_time')

    # ### end Alembic commands ###
