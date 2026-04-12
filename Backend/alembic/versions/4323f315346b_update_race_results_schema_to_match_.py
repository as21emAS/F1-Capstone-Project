"""update_race_results_schema_to_match_data_contract

Revision ID: 4323f315346b
Revises: 272644a8c576
Create Date: 2026-04-12 18:43:59.723461

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4323f315346b'
down_revision: Union[str, Sequence[str], None] = '272644a8c576'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema to match data contract for race_results table."""
    # Add missing columns
    op.add_column('race_results', sa.Column('circuit_id', sa.String(length=100), nullable=True))
    op.add_column('race_results', sa.Column('race_date', sa.Date(), nullable=True))
    op.add_column('race_results', sa.Column('weather_condition', sa.String(length=50), nullable=True))
    
    # Change grid_position from INTEGER to FLOAT
    op.alter_column('race_results', 'grid_position',
                    existing_type=sa.Integer(),
                    type_=sa.Float(),
                    existing_nullable=True)
    
    # Change finish_position from INTEGER to FLOAT
    op.alter_column('race_results', 'finish_position',
                    existing_type=sa.Integer(),
                    type_=sa.Float(),
                    existing_nullable=True)
    
    # Rename points to points_scored and change to FLOAT
    op.alter_column('race_results', 'points',
                    new_column_name='points_scored',
                    existing_type=sa.Numeric(precision=5, scale=2),
                    type_=sa.Float(),
                    existing_nullable=True)
    
    # Drop columns not in data contract (optional - keeping for backward compatibility)
    # Uncomment below if you want to strictly enforce the data contract:
    # op.drop_column('race_results', 'position_text')
    # op.drop_column('race_results', 'laps_completed')
    # op.drop_column('race_results', 'status')
    # op.drop_column('race_results', 'time')
    # op.drop_column('race_results', 'finished')
    # op.drop_column('race_results', 'dnf')
    
    # Add foreign key for circuit_id
    op.create_foreign_key('fk_race_results_circuit_id', 'race_results', 'circuits', ['circuit_id'], ['circuit_id'])


def downgrade() -> None:
    """Downgrade schema."""
    # Drop foreign key
    op.drop_constraint('fk_race_results_circuit_id', 'race_results', type_='foreignkey')
    
    # Rename points_scored back to points and change to Numeric
    op.alter_column('race_results', 'points_scored',
                    new_column_name='points',
                    existing_type=sa.Float(),
                    type_=sa.Numeric(precision=5, scale=2),
                    existing_nullable=True)
    
    # Change finish_position back to INTEGER
    op.alter_column('race_results', 'finish_position',
                    existing_type=sa.Float(),
                    type_=sa.Integer(),
                    existing_nullable=True)
    
    # Change grid_position back to INTEGER
    op.alter_column('race_results', 'grid_position',
                    existing_type=sa.Float(),
                    type_=sa.Integer(),
                    existing_nullable=True)
    
    # Drop added columns
    op.drop_column('race_results', 'weather_condition')
    op.drop_column('race_results', 'race_date')
    op.drop_column('race_results', 'circuit_id')
