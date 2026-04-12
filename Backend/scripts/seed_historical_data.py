import sys
import os
from pathlib import Path
from datetime import datetime

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import func
from database.database import SessionLocal, engine
from app.models.models import Base, Circuit, Race, Driver, Team, RaceResult, DriverStanding, TeamStanding
from app.external.jolpica import JolpicaF1Client
from app.external.transformers import (
    transform_race,
    transform_driver,
    transform_team,
    transform_result
)

# Configuration
SEASONS_TO_SEED = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017,
                   2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]  # Historical seasons
CURRENT_SEASON = 2026  # Current season for standings

def create_tables():
    print("Creating database tables...")
    Base.metadata.create_all(engine)
    print("Tables created")

def seed_circuits_for_seasons(session, client, seasons):
    # Seed circuits from multiple seasons
    print(f"\nSeeding circuits from {len(seasons)} seasons...")
    
    all_circuits = {}
    circuits_added = 0
    circuits_updated = 0
    
    for year in seasons:
        print(f"  Fetching {year} circuits...")
        races = client.get_race_schedule(year)
        
        for race in races:
            circuit_data = race.get('Circuit', {})
            location_data = circuit_data.get('Location', {})
            circuit_id = circuit_data.get('circuitId')
            
            if not circuit_id or circuit_id in all_circuits:
                continue
            
            all_circuits[circuit_id] = True
            
            existing_circuit = session.query(Circuit).filter_by(circuit_id=circuit_id).first()
            
            if existing_circuit:
                existing_circuit.circuit_name = circuit_data.get('circuitName', '')
                existing_circuit.location = location_data.get('locality', '')
                existing_circuit.country = location_data.get('country', '')
                existing_circuit.latitude = float(location_data.get('lat', 0)) if location_data.get('lat') else None
                existing_circuit.longitude = float(location_data.get('long', 0)) if location_data.get('long') else None
                existing_circuit.updated_at = datetime.now()
                circuits_updated += 1
            else:
                circuit_obj = Circuit(
                    circuit_id=circuit_id,
                    circuit_name=circuit_data.get('circuitName', ''),
                    location=location_data.get('locality', ''),
                    country=location_data.get('country', ''),
                    latitude=float(location_data.get('lat', 0)) if location_data.get('lat') else None,
                    longitude=float(location_data.get('long', 0)) if location_data.get('long') else None
                )
                session.add(circuit_obj)
                circuits_added += 1
    
    session.commit()
    print(f"Circuits: {circuits_added} added, {circuits_updated} updated")
    return circuits_added + circuits_updated


def seed_races_for_seasons(session, client, seasons):
    # Seed races from multiple seasons
    print(f"\n Seeding races from {len(seasons)} seasons...")
    
    total_races_added = 0
    total_races_updated = 0
    
    for year in seasons:
        print(f" Fetching {year} season races...")
        races = client.get_race_schedule(year)
        
        for race_data in races:
            circuit_data = race_data.get('Circuit', {})
            location_data = circuit_data.get('Location', {})
            
            year_val = int(race_data.get('season', year))
            round_val = int(race_data.get('round', 0))
            
            existing_race = session.query(Race).filter_by(
                year=year_val,
                round=round_val
            ).first()
            
            date_str = race_data.get('date')
            race_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
            
            if existing_race:
                existing_race.race_name = race_data.get('raceName', '')
                existing_race.circuit_id = circuit_data.get('circuitId', '')
                existing_race.circuit_name = circuit_data.get('circuitName', '')
                existing_race.country = location_data.get('country', '')
                existing_race.date = race_date
                existing_race.updated_at = datetime.now()
                total_races_updated += 1
            else:

                race_obj = Race(
                    year=year_val,
                    round=round_val,
                    race_name=race_data.get('raceName', ''),
                    circuit_id=circuit_data.get('circuitId', ''),
                    circuit_name=circuit_data.get('circuitName', ''),
                    country=location_data.get('country', ''),
                    date=race_date
                )
                session.add(race_obj)
                total_races_added += 1
        
        session.commit()
        print(f"  ✅ {year}: {len(races)} races processed")
    
    print(f"✅ Total Races: {total_races_added} added, {total_races_updated} updated")
    return total_races_added + total_races_updated


def seed_drivers_for_seasons(session, client, seasons):
    # Seed drivers from multiple seasons
    print(f"\n Seeding drivers from {len(seasons)} seasons...")
    
    all_drivers = {}  # Track drivers we've already processed
    drivers_added = 0
    drivers_updated = 0
    
    for year in seasons:
        print(f"  Fetching {year} drivers...")
        drivers = client.get_all_drivers(year)
        
        for driver_data in drivers:
            driver_id = driver_data.get('driverId')
            
            if not driver_id:
                continue
            
            if driver_id in all_drivers:
                continue
            
            all_drivers[driver_id] = True
            existing_driver = session.query(Driver).filter_by(driver_id=driver_id).first()
            
            if existing_driver:
                existing_driver.driver_number = driver_data.get('permanentNumber')
                existing_driver.driver_code = driver_data.get('code')
                existing_driver.driver_forename = driver_data.get('givenName', '')
                existing_driver.driver_surname = driver_data.get('familyName', '')
                existing_driver.driver_full_name = f"{driver_data.get('givenName', '')} {driver_data.get('familyName', '')}"
                existing_driver.nationality = driver_data.get('nationality', '')
                existing_driver.updated_at = datetime.now()
                drivers_updated += 1
            else:
                driver_obj = Driver(
                    driver_id=driver_id,
                    driver_number=driver_data.get('permanentNumber'),
                    driver_code=driver_data.get('code'),
                    driver_forename=driver_data.get('givenName', ''),
                    driver_surname=driver_data.get('familyName', ''),
                    driver_full_name=f"{driver_data.get('givenName', '')} {driver_data.get('familyName', '')}",
                    nationality=driver_data.get('nationality', '')
                )
                session.add(driver_obj)
                drivers_added += 1
        
        session.commit()
    
    print(f"✅ Drivers: {drivers_added} added, {drivers_updated} updated")
    return drivers_added + drivers_updated


def seed_teams_for_seasons(session, client, seasons):
    # Seed teams from multiple seasons
    print(f"\n Seeding teams from {len(seasons)} seasons...")
    
    all_teams = {}
    teams_added = 0
    teams_updated = 0
    
    for year in seasons:
        print(f"  Fetching {year} constructors...")
        teams = client.get_all_constructors(year)
        
        for team_data in teams:
            team_id = team_data.get('constructorId')
            
            if not team_id:
                continue
            
            if team_id in all_teams:
                continue
            
            all_teams[team_id] = True
            
            existing_team = session.query(Team).filter_by(team_id=team_id).first()
            
            if existing_team:
                existing_team.team_name = team_data.get('name', '')
                existing_team.updated_at = datetime.now()
                teams_updated += 1
            else:
                team_obj = Team(
                    team_id=team_id,
                    team_name=team_data.get('name', '')
                )
                session.add(team_obj)
                teams_added += 1
        
        session.commit()
    
    print(f"✅ Teams: {teams_added} added, {teams_updated} updated")
    return teams_added + teams_updated


def seed_race_results_for_seasons(session, client, seasons):
    # Seed race results from multiple seasons
    print(f"\n Seeding race results from {len(seasons)} seasons...")
    
    total_results_added = 0
    total_results_updated = 0
    
    for year in seasons:
        print(f"  Processing {year} season results...")
        races = client.get_race_schedule(year)
        
        for race_data in races:
            round_num = int(race_data.get('round', 0))
            
            # Get race from database
            race = session.query(Race).filter_by(year=year, round=round_num).first()
            if not race:
                print(f" Race not found: {year} Round {round_num}")
                continue
            
            # Fetch results for this race
            print(f" Fetching Round {round_num} results...")
            results = client.get_race_results(year, round_num)
            
            for result_data in results:
                driver_data = result_data.get('Driver', {})
                constructor_data = result_data.get('Constructor', {})
                
                driver_id = driver_data.get('driverId')
                team_id = constructor_data.get('constructorId')
                position = result_data.get('position')
                
                # Check if result already exists
                existing_result = session.query(RaceResult).filter_by(
                    race_id=race.race_id,
                    driver_id=driver_id
                ).first()
                
                # Determine finish status
                status = result_data.get('status', '')
                dnf_keywords = ['Retired', 'Accident', 'Collision', 'Engine', 'Gearbox', 'Spun off', 'Damage']
                is_dnf = any(keyword in status for keyword in dnf_keywords)
                finished = position is not None and not is_dnf
                
                if existing_result:
                    # Update
                    existing_result.team_id = team_id
                    existing_result.grid_position = int(result_data.get('grid', 0))
                    existing_result.finish_position = int(position) if position else None
                    existing_result.position_text = result_data.get('positionText', '')
                    existing_result.points_scored = float(result_data.get('points', 0))
                    existing_result.laps_completed = int(result_data.get('laps', 0))
                    existing_result.status = status
                    existing_result.time = result_data.get('Time', {}).get('time')
                    existing_result.finished = finished
                    existing_result.dnf = is_dnf
                    existing_result.updated_at = datetime.now()
                    total_results_updated += 1
                else:
                    # Add
                    result_obj = RaceResult(
                        race_id=race.race_id,
                        driver_id=driver_id,
                        team_id=team_id,
                        grid_position=int(result_data.get('grid', 0)),
                        finish_position=int(position) if position else None,
                        position_text=result_data.get('positionText', ''),
                        points_scored=float(result_data.get('points', 0)),
                        laps_completed=int(result_data.get('laps', 0)),
                        status=status,
                        time=result_data.get('Time', {}).get('time'),
                        finished=finished,
                        dnf=is_dnf
                    )
                    session.add(result_obj)
                    total_results_added += 1
            
            session.commit()
        
        print(f"✅ {year}: Results processed")
    
    print(f"✅ Total Results: {total_results_added} added, {total_results_updated} updated")
    return total_results_added + total_results_updated


def seed_current_standings(session, client, year):
    # Seed current season standings
    print(f"\n Seeding {year} current standings...")
    
    # Driver standings
    driver_standings = client.get_driver_standings(year)
    driver_standings_added = 0
    
    for standing in driver_standings:
        driver_data = standing.get('Driver', {})
        driver_id = driver_data.get('driverId')
        
        existing = session.query(DriverStanding).filter_by(
            year=year,
            driver_id=driver_id
        ).first()
        
        if existing:
            existing.position = int(standing.get('position', 0))
            existing.points = float(standing.get('points', 0))
            existing.wins = int(standing.get('wins', 0))
            existing.updated_at = datetime.now()
        else:
            standing_obj = DriverStanding(
                year=year,
                driver_id=driver_id,
                position=int(standing.get('position', 0)),
                points=float(standing.get('points', 0)),
                wins=int(standing.get('wins', 0))
            )
            session.add(standing_obj)
            driver_standings_added += 1
    
    session.commit()
    print(f" Driver standings: {driver_standings_added} entries")
    
    # Constructor standings
    team_standings = client.get_constructor_standings(year)
    team_standings_added = 0
    
    for standing in team_standings:
        constructor_data = standing.get('Constructor', {})
        team_id = constructor_data.get('constructorId')
        
        existing = session.query(TeamStanding).filter_by(
            year=year,
            team_id=team_id
        ).first()
        
        if existing:
            existing.position = int(standing.get('position', 0))
            existing.points = float(standing.get('points', 0))
            existing.wins = int(standing.get('wins', 0))
            existing.updated_at = datetime.now()
        else:
            standing_obj = TeamStanding(
                year=year,
                team_id=team_id,
                position=int(standing.get('position', 0)),
                points=float(standing.get('points', 0)),
                wins=int(standing.get('wins', 0))
            )
            session.add(standing_obj)
            team_standings_added += 1
    
    session.commit()
    print(f"✅ Team standings: {team_standings_added} entries")

# Main func
def seed_historical_data():
    # Main seeding function
    print("\n" + "="*70)
    print("F1 HISTORICAL DATA SEEDER (2020-2026)")
    print("="*70)
    
    # Initialize API client with retry and rate limiting
    print("\n   Initializing Jolpica F1 API client...")
    print("   Rate limit: 2 calls/second")
    print("   Cache: 6 hour TTL")
    print("   Retry: Up to 3 attempts with exponential backoff")
    client = JolpicaF1Client(cache_hours=6, calls_per_second=2.0)
    
    # Creates database session
    session = SessionLocal()
    
    try:
        # Create tables
        create_tables()
        
        # Seed data
        circuits_count = seed_circuits_for_seasons(session, client, SEASONS_TO_SEED + [CURRENT_SEASON])
        races_count = seed_races_for_seasons(session, client, SEASONS_TO_SEED + [CURRENT_SEASON])
        drivers_count = seed_drivers_for_seasons(session, client, SEASONS_TO_SEED + [CURRENT_SEASON])
        teams_count = seed_teams_for_seasons(session, client, SEASONS_TO_SEED + [CURRENT_SEASON])
        results_count = seed_race_results_for_seasons(session, client, SEASONS_TO_SEED)  # historical only

        # Seed current season standings
        seed_current_standings(session, client, CURRENT_SEASON)
        
        # Final summary
        print("\n" + "="*70)
        print("SEEDING COMPLETE")
        print("="*70)
        print(f"\n Summary:")
        print(f"   Seasons seeded: {', '.join(map(str, SEASONS_TO_SEED + [CURRENT_SEASON]))}")
        print(f"   Circuits: {circuits_count}")
        print(f"   Races: {races_count}")
        print(f"   Drivers: {drivers_count}")
        print(f"   Teams: {teams_count}")
        print(f"   Race Results: {results_count}")
        print(f"   Current standings: {CURRENT_SEASON}")
        print(f"\n Database is ready for frontend.")
        print(f"   - GET /api/standings/drivers/current → {CURRENT_SEASON} driver standings")
        print(f"   - GET /api/standings/teams/current → {CURRENT_SEASON} team standings")
        print(f"   - GET /api/races/next → Next upcoming race")
        print(f"   - Historical data: {SEASONS_TO_SEED[0]}-{SEASONS_TO_SEED[-1]}")
        print("\n")
        
    except Exception as e:
        print(f"\n ERROR: {e}")
        session.rollback()
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        session.close()


if __name__ == "__main__":
    seed_historical_data()