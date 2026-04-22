"""add_timezone_to_circuits

Revision ID: c6513ee7b293
Revises: 2d12a0aaec85
Create Date: 2026-04-22 14:35:04.224179

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6513ee7b293'
down_revision: Union[str, Sequence[str], None] = '2d12a0aaec85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add timezone column to circuits table."""
    # Add timezone column
    op.add_column('circuits', sa.Column('timezone', sa.String(50), nullable=True))
    
    # Populate common F1 circuit timezones using IANA timezone identifiers
    # These automatically handle Daylight Saving Time (DST)
    timezone_mappings = {
        'Bahrain': 'Asia/Bahrain',
        'Saudi Arabia': 'Asia/Riyadh',
        'Australia': 'Australia/Melbourne',
        'Japan': 'Asia/Tokyo',
        'China': 'Asia/Shanghai',
        'USA': 'America/New_York',  # Miami
        'Italy': 'Europe/Rome',  # Imola
        'Monaco': 'Europe/Monaco',
        'Spain': 'Europe/Madrid',  # Barcelona
        'Canada': 'America/Montreal',
        'Austria': 'Europe/Vienna',
        'UK': 'Europe/London',  # Silverstone
        'Hungary': 'Europe/Budapest',
        'Belgium': 'Europe/Brussels',
        'Netherlands': 'Europe/Amsterdam',
        'Azerbaijan': 'Asia/Baku',
        'Singapore': 'Asia/Singapore',
        'Mexico': 'America/Mexico_City',
        'Brazil': 'America/Sao_Paulo',
        'UAE': 'Asia/Dubai',  # Abu Dhabi
        'United States': 'America/New_York',  # Austin, Las Vegas, Miami variants
    }
    
    # Update circuits with timezone based on country
    for country, timezone in timezone_mappings.items():
        op.execute(
            f"UPDATE circuits SET timezone = '{timezone}' WHERE country = '{country}'"
        )


def downgrade() -> None:
    """Remove timezone column from circuits table."""
    op.drop_column('circuits', 'timezone')
