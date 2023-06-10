"""empty message

Revision ID: 265928c63a7f
Revises: ade1657d4eed
Create Date: 2022-05-21 19:35:32.385924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '265928c63a7f'
down_revision = 'ade1657d4eed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_venue', sa.String(), nullable=True))
    op.add_column('Venue', sa.Column('seeking_talent', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'seeking_talent')
    op.drop_column('Artist', 'seeking_venue')
    # ### end Alembic commands ###