"""populate skate position columns

Revision ID: 502fee06b176
Revises: 516fb37c0e42
Create Date: 2025-02-07 16:20:18.400732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '502fee06b176'
down_revision: Union[str, None] = '516fb37c0e42'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        """
        WITH ranked_skates AS (
            SELECT id, 
                   row_number() OVER (PARTITION BY event_id ORDER BY id) AS skate_position
            FROM skates
        )
        UPDATE skates e
        SET skate_position = re.skate_position
        FROM ranked_skates re
        WHERE e.id = re.id
        """
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
