"""revised model column names

Revision ID: 950311770403
Revises: 5bb897a7e91d
Create Date: 2024-05-15 20:38:07.442309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '950311770403'
down_revision: Union[str, None] = '5bb897a7e91d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('events', 'evt_number', nullable=False, new_column_name='event_number')
    op.alter_column('events', 'evt_title', nullable=False, new_column_name='event_name')
    op.alter_column('skates', 'evt_id', nullable=False, new_column_name='event_id')
    op.alter_column('skates', 'skater', nullable=False, new_column_name='skater_name')
    op.alter_column('files', 'file', nullable=False, new_column_name='file_name')


def downgrade() -> None:
    pass
