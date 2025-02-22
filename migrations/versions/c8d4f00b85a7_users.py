"""users

Revision ID: c8d4f00b85a7
Revises: f346cf8d2641
Create Date: 2023-08-20 15:38:22.653050

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8d4f00b85a7'
down_revision: Union[str, None] = 'f346cf8d2641'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_traveler_expert')
    op.drop_column('users', 'phone_number')
    op.drop_column('users', 'is_traveler')
    op.drop_column('users', 'company_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('company_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('is_traveler', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('phone_number', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('is_traveler_expert', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
