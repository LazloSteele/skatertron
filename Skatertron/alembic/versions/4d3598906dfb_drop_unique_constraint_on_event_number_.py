"""drop unique constraint on event number column

Revision ID: 4d3598906dfb
Revises: 950311770403
Create Date: 2024-05-15 21:15:41.950446

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d3598906dfb'
down_revision: Union[str, None] = '950311770403'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('events_evt_number_key', 'events')


def downgrade() -> None:
    op.create_unique_constraint('events_evt_number_key', 'events', ['evt_number'])
