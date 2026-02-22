"""add team_id and nationality to drivers

Revision ID: 7b15eb255dd0
Revises: a93200edc9a1
Create Date: 2026-02-21 19:18:02.947872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b15eb255dd0'
down_revision: Union[str, Sequence[str], None] = 'a93200edc9a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('drivers', sa.Column('nationality', sa.String(100), nullable=True))
    op.add_column('drivers', sa.Column('team_id', sa.String(100), nullable=True))
    op.create_foreign_key('fk_drivers_team_id', 'drivers', 'teams', ['team_id'], ['team_id'])

def downgrade() -> None:
    op.drop_constraint('fk_drivers_team_id', 'drivers', type_='foreignkey')
    op.drop_column('drivers', 'team_id')
    op.drop_column('drivers', 'nationality')
