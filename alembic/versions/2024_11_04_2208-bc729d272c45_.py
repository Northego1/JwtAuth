"""empty message

Revision ID: bc729d272c45
Revises: b0899e322a4f
Create Date: 2024-11-04 22:08:14.245828

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc729d272c45'
down_revision: Union[str, None] = 'b0899e322a4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the old table
    op.drop_table('black_list_access_jwt')

    # Create the new table with the updated schema
    op.create_table(
        'black_list_access_jwt',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=sa.text('uuid_generate_v4()')),
        sa.Column('access_token', sa.String, nullable=False),
        sa.Column('expire_at', sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    # Drop the new table
    op.drop_table('black_list_access_jwt')

    # Recreate the old table with INTEGER id
    op.create_table(
        'black_list_access_jwt',
        sa.Column('id', sa.INTEGER, primary_key=True, autoincrement=True),
        sa.Column('access_token', sa.String, nullable=False),
        sa.Column('expire_at', sa.DateTime, nullable=False),
    )