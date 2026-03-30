#More testing of API client and data transformers

from app.external.jolpica import JolpicaF1Client
from app.external.transformers import transform_race, transform_result, transform_driver, transform_team

client = JolpicaF1Client()

# Test 1: Next Race
print("TEST 1: Next Race Information")
print("-" * 70)
next_race = client.get_next_race()
if next_race:
    transformed = transform_race(next_race)
    print(f"✅ Next Race:")
    print(f"   {transformed['race_name']}")
    print(f"   {transformed['circuit_name']}, {transformed['country']}")
    print(f"   Date: {transformed['date']}")
else:
    print("Error: No upcoming race (off-season)")

# Test 2: Most recent season data (2025)
print("\n\nTEST 2: Current Season (2025 Season)")
print("-" * 70)

races_2025 = client.get_current_season_races()
print(f"✅ 2025 Race Calendar: {len(races_2025)} races")

drivers_2025 = client.get_all_drivers()
print(f"✅ Current Drivers: {len(drivers_2025)} drivers")

teams_2025 = client.get_all_constructors()
print(f"✅ Current Teams: {len(teams_2025)} teams")

# Test 3: Historical Data (for ML training)
print("\n\nTEST 3: Historical Data (2024 Season)")
print("-" * 70)

races_2024 = client.get_season_races(2024)
print(f"2024 Races: {len(races_2024)} races")

results_2024_bahrain = client.get_race_results(2024, 1)
print(f"2024 Bahrain GP Results: {len(results_2024_bahrain)} drivers")

standings_2024 = client.get_driver_standings(2024)
print(f"2024 Final Standings: {len(standings_2024)} drivers")

# Test 4: Data Transformation
print("\n\nTEST 4: Data Transformation (Database Format)")
print("-" * 70)

# Transform race
if races_2024:
    race_data = transform_race(races_2024[0])
    print("✅ Transformed Race:")
    for key, value in race_data.items():
        print(f"   {key}: {value}")

print()

# Transform result
if results_2024_bahrain:
    result_data = transform_result(results_2024_bahrain[0])
    print("✅ Transformed Race Result:")
    print(f"   Driver: {result_data['driver_full_name']}")
    print(f"   Team: {result_data['team_name']}")
    print(f"   Grid Position: {result_data['grid_position']}")
    print(f"   Finish Position: {result_data['finish_position']}")
    print(f"   Points: {result_data['points']}")
    print(f"   Laps Completed: {result_data['laps_completed']}")
    print(f"   Finished: {result_data['finished']}")
    print(f"   DNF: {result_data['dnf']}")

# Test 5: All Data Available
print("\n\nTEST 5: Data Coverage Check")
print("-" * 70)

# Check multiple seasons
seasons_available = []
for year in [2020, 2021, 2022, 2023, 2024, 2025]:
    races = client.get_season_races(year)
    if races:
        seasons_available.append(year)
        print(f"{year} Season: {len(races)} races available")

print("\n")