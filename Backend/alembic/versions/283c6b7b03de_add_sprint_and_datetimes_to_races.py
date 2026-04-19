"""add_sprint_and_datetimes_to_races

Revision ID: 283c6b7b03de
Revises: 4323f315346b
Create Date: 2026-04-19 14:07:02.515836

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '283c6b7b03de'
down_revision: Union[str, Sequence[str], None] = '4323f315346b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('races', sa.Column('start_datetime', sa.DateTime(timezone=True), nullable=True))
    op.add_column('races', sa.Column('end_datetime', sa.DateTime(timezone=True), nullable=True))
    op.add_column('races', sa.Column('is_sprint', sa.Boolean(), server_default='false', nullable=False))

def downgrade() -> None:
    op.drop_column('races', 'is_sprint')
    op.drop_column('races', 'end_datetime')
    op.drop_column('races', 'start_datetime')