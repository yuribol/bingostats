"""Create local nginx table

Revision ID: 00f178d72715
Revises: 
Create Date: 2020-02-12 10:12:22.215930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00f178d72715'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    op.create_table('local_ngrok',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=64), nullable=False),
                    sa.Column('ngrok_url', sa.String(length=120), nullable=False),
                    sa.PrimaryKeyConstraint('id'))

    op.create_index(op.f('ix_name'), 'local_ngrok', ['name'], unique=True)


def downgrade():
    pass
