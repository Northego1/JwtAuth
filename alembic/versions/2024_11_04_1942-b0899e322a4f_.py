"""empty message

Revision ID: b0899e322a4f
Revises: ab2a2902e70f
Create Date: 2024-11-04 19:42:58.714551

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b0899e322a4f'
down_revision: Union[str, None] = 'ab2a2902e70f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('black_list_access_jwt_expire_at_key', 'black_list_access_jwt', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('black_list_access_jwt_expire_at_key', 'black_list_access_jwt', ['expire_at'])
    # ### end Alembic commands ###