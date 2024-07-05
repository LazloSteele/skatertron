"""Add file_path and file_type columns to file data model

Revision ID: c9502521e560
Revises: 4d3598906dfb
Create Date: 2024-07-05 15:39:38.662537

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9502521e560'
down_revision: Union[str, None] = '4d3598906dfb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('files', sa.Column('file_path', sa.String))
    op.add_column('files', sa.Column('file_type', sa.String))


def downgrade() -> None:
    pass
