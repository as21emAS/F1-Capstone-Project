import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from app.services.db_writer import upsert_driver_standings, upsert_constructor_standings, upsert_race_results
# Test driver standings
test_drivers = [
    {'year': 2026, 'driver_id': 'max_verstappen', 'position': 1, 'points': 575.0, 'wins': 19, 'team_id': 'red_bull'},
    {'year': 2026, 'driver_id': 'hamilton', 'position': 2, 'points': 400.0, 'wins': 5, 'team_id': 'ferrari'},
]

# Test constructor standings
test_teams = [
    {'year': 2026, 'team_id': 'red_bull', 'position': 1, 'points': 860.0, 'wins': 21},
    {'year': 2026, 'team_id': 'ferrari', 'position': 2, 'points': 600.0, 'wins': 8},
]

# Test race results
test_results = [
    {
        'race_id': 332,
        'circuit_id': 'Japan',
        'race_date': '2026-05-26',
        'driver_id': 'max_verstappen',
        'team_id': 'red_bull',
        'grid_position': 1.0,
        'finish_position': 1.0,
        'points_scored': 25.0,
        'position_text': '1',
        'laps_completed': 78,
        'status': 'Finished',
        'time': '1:42:12.345',
        'dnf': False,
        'weather_condition': 'dry'
    }
]

print("Testing upsert_driver_standings...")
count = upsert_driver_standings(test_drivers)
print(f"✅ {count} rows upserted")

print("Testing upsert_constructor_standings...")
count = upsert_constructor_standings(test_teams)
print(f"✅ {count} rows upserted")

print("Testing upsert_race_results...")
count = upsert_race_results(test_results)
print(f"✅ {count} rows inserted")

print("\nAll tests passed!")