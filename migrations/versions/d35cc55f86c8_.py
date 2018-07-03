"""empty message

Revision ID: d35cc55f86c8
Revises: 1167d6904199
Create Date: 2018-07-02 23:02:46.142954

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd35cc55f86c8'
down_revision = '1167d6904199'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'RideOffer', 'users', ['driver_email'], ['email'])
    op.create_foreign_key(None, 'RideRequest', 'RideOffer', ['ride_offer_id'], ['ride_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'RideRequest', type_='foreignkey')
    op.drop_constraint(None, 'RideOffer', type_='foreignkey')
    # ### end Alembic commands ###
