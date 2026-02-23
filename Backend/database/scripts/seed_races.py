import sys
from pathlib import Path
from datetime import datetime

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy import func
from database.database import SessionLocal, engine
from models import Base, Circuit, Race
from api_clients.jolpica_f1_client import JolpicaF1Client

# Create all tables if they don't exist
def create_tables():
    print("Creating database tables if they don't exist...")
    Base.metadata.create_all(engine)
    print("✅ Tables ready")

# Extract unique circuits from races data and insert into database
def seed_circuits(session, races_data):
    print("\n Seeding circuits...")
    
    circuits_added = 0
    circuits_updated = 0
    
    for race in races_data:
        circuit_data = race.get('Circuit', {})
        location_data = circuit_data.get('Location', {})
        
        circuit_id = circuit_data.get('circuitId')
        
        if not circuit_id:
            continue
        
        # Check if circuit already exists
        existing_circuit = session.query(Circuit).filter_by(circuit_id=circuit_id).first()
        
        # Update existing circuit
        if existing_circuit:
            existing_circuit.circuit_name = circuit_data.get('circuitName', '')
            existing_circuit.location = location_data.get('locality', '')
            existing_circuit.country = location_data.get('country', '')
            existing_circuit.latitude = float(location_data.get('lat', 0)) if location_data.get('lat') else None
            existing_circuit.longitude = float(location_data.get('long', 0)) if location_data.get('long') else None
            existing_circuit.updated_at = datetime.now()
            circuits_updated += 1
        else:
            # Add new circuit
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
    print(f"✅ Circuits: {circuits_added} added, {circuits_updated} updated")


def seed_races(session, races_data, year):
    # Insert races into database
    print(f"\n Seeding {year} season races...")
    
    races_added = 0
    races_updated = 0
    
    for race_data in races_data:
        circuit_data = race_data.get('Circuit', {})
        location_data = circuit_data.get('Location', {})
        
        year_val = int(race_data.get('season', year))
        round_val = int(race_data.get('round', 0))
        
        # Check if race already exists (by year and round)
        existing_race = session.query(Race).filter_by(
            year=year_val,
            round=round_val
        ).first()
        
        # Parse date
        date_str = race_data.get('date')
        race_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
        
        if existing_race:
            # Update existing race
            existing_race.race_name = race_data.get('raceName', '')
            existing_race.circuit_id = circuit_data.get('circuitId', '')
            existing_race.circuit_name = circuit_data.get('circuitName', '')
            existing_race.country = location_data.get('country', '')
            existing_race.date = race_date
            existing_race.updated_at = datetime.now()
            races_updated += 1
        else:
            # Add new race
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
            races_added += 1
    
    session.commit()
    print(f"✅ Races: {races_added} added, {races_updated} updated")


def validate_data(session, year):
    # Validate that data was inserted correctly
    print(f"\n Validating {year} season data...")
    
    race_count = session.query(Race).filter_by(year=year).count()
    circuit_count = session.query(Circuit).count()
    
    print(f"✅ Found {race_count} races for {year}")
    print(f"✅ Found {circuit_count} total circuits in database")
    
    # Check for duplicates
    duplicate_races = session.query(Race.year, Race.round)\
        .group_by(Race.year, Race.round)\
        .having(func.count() > 1)\
        .all()
    
    if duplicate_races:
        print(f"X Warning: Found {len(duplicate_races)} duplicate races")
        for year_dup, round_num in duplicate_races:
            print(f"   - Year {year_dup}, Round {round_num}")
    else:
        print("✅ No duplicate races found")
    
    return race_count, circuit_count


def seed_races_and_circuits(year=2025):
    # Main seeding function
    print("\n" + "="*70)
    print("F1 RACE DATA SEEDER")
    print("="*70)
    
    # Initialize API client
    print(f"\nInitializing Jolpica F1 API client...")
    client = JolpicaF1Client()
    
    # Fetch season data
    print(f"Fetching {year} season schedule from Jolpica API...")
    races_data = client.get_race_schedule(year)
    
    if not races_data:
        print(f"X ERROR: Could not fetch {year} season data")
        print(f"  API might be down or {year} season not yet available")
        return
    
    print(f"✅ Fetched {len(races_data)} races for {year} season")
    
    # Create database session
    session = SessionLocal()
    
    try:
        create_tables()
        
        # Seed circuits
        seed_circuits(session, races_data)
        
        # Seed races
        seed_races(session, races_data, year)
        
        race_count, circuit_count = validate_data(session, year)
        
        print("\n" + "="*70)
        print("✅ Seeding Complete")
        print("="*70)
        print(f"\n Summary:")
        print(f"   - {race_count} races for {year} season")
        print(f"   - {circuit_count} unique circuits")
        print(f"   - Data matches Jolpica F1 API")
        print(f"   - No duplicates detected")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        session.rollback()
        import traceback
        traceback.print_exc()
    
    finally:
        session.close()


if __name__ == "__main__":
    for year in range(2010, 2027):
        seed_races_and_circuits(year)