"""add_unique_constraints_to_standings

Revision ID: 2d12a0aaec85
Revises: 283c6b7b03de
Create Date: 2026-04-20 01:40:56.840100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d12a0aaec85'
down_revision: Union[str, Sequence[str], None] = '283c6b7b03de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add unique constraint to driver_standings (year, driver_id)
    op.create_unique_constraint(
        'uq_driver_standings_year_driver',
        'driver_standings',
        ['year', 'driver_id']
    )
    
    # Add unique constraint to team_standings (year, team_id)
    op.create_unique_constraint(
        'uq_team_standings_year_team',
        'team_standings',
        ['year', 'team_id']
    )
    
    # Add unique constraint to race_results (race_id, driver_id)
    op.create_unique_constraint(
        'uq_race_results_race_driver',
        'race_results',
        ['race_id', 'driver_id']
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove constraints in reverse order
    op.drop_constraint('uq_race_results_race_driver', 'race_results', type_='unique')
    op.drop_constraint('uq_team_standings_year_team', 'team_standings', type_='unique')
    op.drop_constraint('uq_driver_standings_year_driver', 'driver_standings', type_='unique')