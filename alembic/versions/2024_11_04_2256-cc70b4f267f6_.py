"""empty message

Revision ID: cc70b4f267f6
Revises: bc729d272c45
Create Date: 2024-11-04 22:56:52.734616

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc70b4f267f6'
down_revision: Union[str, None] = 'bc729d272c45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'black_list_access_jwt', ['access_token'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'black_list_access_jwt', type_='unique')
    # ### end Alembic commands ###
