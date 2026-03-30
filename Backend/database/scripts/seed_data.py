import sys
from pathlib import Path

# Add backend root to path so all imports resolve
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.external.jolpica import JolpicaF1Client
from app.external.transformers import transform_team, transform_driver
from database.crud import upsert_team, upsert_driver


def seed_teams_and_drivers(year=2024):
    client = JolpicaF1Client()

    # Teams first (drivers FK depends on teams existing)
    print(f"Seeding teams for {year}...")
    teams = client.get_all_constructors(year)
    for team in teams:
        upsert_team(transform_team(team))
    print(f"✅ {len(teams)} teams inserted/updated")

    # Then drivers
    print(f"Seeding drivers for {year}...")
    drivers = client.get_all_drivers(year)
    for driver in drivers:
        upsert_driver(transform_driver(driver))
    print(f"✅ {len(drivers)} drivers inserted/updated")


if __name__ == "__main__":
    for year in range(2010, 2027):
        seed_teams_and_drivers(year)