"""Change footage exceptions to no_video

Revision ID: 96052d621d1e
Revises: 314758b3689d
Create Date: 2025-02-23 19:22:54.612603

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96052d621d1e'
down_revision: Union[str, None] = '314758b3689d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('skates', 'footage_exceptions')
    op.add_column(
        'skates',
        sa.Column(
            'no_video',
            sa.Boolean(),
            nullable=False,
            server_default='false'
        )
    )


def downgrade() -> None:
    pass
