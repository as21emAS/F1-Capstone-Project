import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from api_clients.jolpica_f1_client import JolpicaF1Client
from api_clients.data_transformers import transform_team
from database.crud import upsert_driver, upsert_team

def seed_teams_and_drivers(year=2024):
    client = JolpicaF1Client()
    
    # Teams first (drivers FK depends on teams existing)
    print(f"Seeding teams for {year}...")
    teams = client.get_all_constructors(year)
    for team in teams:
        upsert_team(transform_team(team))
    print(f"✅ {len(teams)} teams inserted")
    
    # Then drivers with nationality + team_id
    print(f"Seeding drivers for {year}...")
    drivers = client.get_drivers_with_teams(year)
    for driver in drivers:
        upsert_driver(driver)
    print(f"✅ {len(drivers)} drivers inserted")

if __name__ == "__main__":
    seed_teams_and_drivers(2024)