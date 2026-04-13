"""
Backfill Historical Weather Data
 
Fetches historical weather for all races in the database and populates weather_data table.
Can be run multiple times safely - skips races that already have weather data.

Usage:
    python scripts/backfill_historical_weather.py [--rate CALLS_PER_SECOND] [--year YEAR]
    
Examples:
    # Conservative (1 call every 2 seconds, overnight completion):
    python scripts/backfill_historical_weather.py
    
    # Aggressive (1 call per second, ~6 minutes):
    python scripts/backfill_historical_weather.py --rate 1.0
    
    # Backfill only 2024 races:
    python scripts/backfill_historical_weather.py --year 2024
"""

import os
import sys
import argparse
from datetime import datetime
from typing import List, Dict, Optional

# add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text, select
from sqlalchemy.orm import Session
from database.database import SessionLocal
from api_clients.visualcrossing_client import VisualCrossingClient
from app.core.config import settings


def get_races_needing_weather(session: Session, year: Optional[int] = None) -> List[Dict]:
    """
    Query races that don't have weather data yet
    
    Args:
        session: Database session
        year: Optional year filter
        
    Returns:
        List of race dicts with id, race_date, circuit name, lat, lon
    """
    query = """
        SELECT 
            r.race_id,
            r.date as race_date,
            r.round,
            c.circuit_name,
            c.circuit_id,
            c.latitude as lat,
            c.longitude as lon
        FROM races r
        JOIN circuits c ON r.circuit_id = c.circuit_id
        LEFT JOIN weather_data wd ON r.race_id = wd.race_id
        WHERE wd.weather_id IS NULL
        AND r.date < CURRENT_DATE
    """
    
    if year:
        query += f" AND EXTRACT(YEAR FROM r.date) = {year}"
    
    query += " ORDER BY r.date DESC"
    
    result = session.execute(text(query))
    rows = result.fetchall()
    
    return [
        {
            'race_id': row.race_id,
            'race_date': row.race_date,
            'round': row.round,
            'circuit_name': row.circuit_name,
            'circuit_id': row.circuit_id,
            'lat': float(row.lat),
            'lon': float(row.lon)
        }
        for row in rows
    ]


def insert_weather_data(session: Session, race_id: int, weather: Dict) -> bool:
    """
    Insert weather data into database
    
    Args:
        session: Database session
        race_id: Race ID
        weather: Weather data dict from Visual Crossing client
        
    Returns:
        True if successful, False otherwise
    """
    try:
        query = text("""
            INSERT INTO weather_data 
            (race_id, temperature, humidity, conditions, wind_speed, rainfall, forecast_time)
            VALUES 
            (:race_id, :temperature, :humidity, :conditions, :wind_speed, :rainfall, :forecast_time)
        """)
        
        session.execute(query, {
            'race_id': race_id,
            'temperature': weather['temperature'],
            'humidity': weather['humidity'],
            'conditions': weather['conditions'],
            'wind_speed': weather['wind_speed'],
            'rainfall': weather['rainfall'],
            'forecast_time': weather['forecast_time']
        })
        
        session.commit()
        return True
        
    except Exception as e:
        session.rollback()
        print(f"  Database error: {e}")
        return False


def backfill_weather(
    api_key: str,
    calls_per_second: float = 0.5,
    year: Optional[int] = None,
    dry_run: bool = False
):
    """
    Main backfill function
    
    Args:
        api_key: Visual Crossing API key
        calls_per_second: API rate limit
        year: Optional year filter
        dry_run: If True, only show what would be done
    """
    print("=" * 70)
    print("F1 HISTORICAL WEATHER BACKFILL")
    print("=" * 70)
    print(f"Rate limit: {calls_per_second} calls/second ({1/calls_per_second:.1f}s between calls)")
    if year:
        print(f"Year filter: {year}")
    if dry_run:
        print("DRY RUN MODE - No data will be written")
    print("=" * 70)
    print()
    
    # Initialize client
    print("Initializing Visual Crossing client...")
    try:
        client = VisualCrossingClient(
            api_key=api_key,
            calls_per_second=calls_per_second,
            cache_days=365
        )
        print("✓ Client ready\n")
    except ValueError as e:
        print(f"✗ Error: {e}")
        return
    
    # Get database session
    session = SessionLocal()
    
    try:
        # Find races needing weather data
        print("Querying races without weather data...")
        races = get_races_needing_weather(session, year=year)
        
        if not races:
            print("✓ All races already have weather data!")
            return
        
        print(f"Found {len(races)} races needing weather data\n")
        
        # Estimate time
        estimated_seconds = len(races) / calls_per_second
        estimated_minutes = estimated_seconds / 60
        
        if estimated_minutes < 60:
            print(f"Estimated time: ~{estimated_minutes:.0f} minutes")
        else:
            print(f"Estimated time: ~{estimated_minutes/60:.1f} hours")
        print()
        
        if dry_run:
            print("DRY RUN - Would fetch weather for these races:")
            for race in races[:10]:  # Show first 10
                print(f"  • {race['race_date']} - {race['circuit_name']}")
            if len(races) > 10:
                print(f"  ... and {len(races) - 10} more")
            return
        
        # Process races
        success_count = 0
        fail_count = 0
        
        for i, race in enumerate(races, 1):
            print(f"\n[{i}/{len(races)}] {race['race_date']} - {race['circuit_name']}")
            
            # Fetch weather
            weather = client.get_historical_weather(
                lat=race['lat'],
                lon=race['lon'],
                race_date=race['race_date']
            )
            
            if not weather:
                print(f"  Failed to fetch weather")
                fail_count += 1
                continue
            
            # insert into database
            print(f"  Inserting: {weather['temperature']}°C, {weather['conditions']}")
            
            if insert_weather_data(session, race['race_id'], weather):
                print(f"  Saved to database")
                success_count += 1
            else:
                fail_count += 1
        
        # summary
        print("\n" + "=" * 70)
        print("BACKFILL COMPLETE")
        print("=" * 70)
        print(f"Success: {success_count}")
        print(f"Failed:  {fail_count}")
        print(f"Total:     {len(races)}")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        print("Progress has been saved. Run again to continue.")
        
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        session.close()


def main():
    """Parse arguments and run backfill"""
    parser = argparse.ArgumentParser(
        description='Backfill historical weather data for F1 races',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Conservative (overnight):
  python scripts/backfill_historical_weather.py
  
  # Aggressive (6 minutes):
  python scripts/backfill_historical_weather.py --rate 1.0
  
  # Backfill only 2024:
  python scripts/backfill_historical_weather.py --year 2024
  
  # Dry run (see what would happen):
  python scripts/backfill_historical_weather.py --dry-run
        """
    )
    
    parser.add_argument(
        '--rate',
        type=float,
        default=0.5,
        help='API calls per second (default: 0.5 = 1 call every 2 seconds)'
    )
    
    parser.add_argument(
        '--year',
        type=int,
        help='Only backfill races from specific year'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
    
    args = parser.parse_args()
    
    # Get API key from settings (automatically loads from .env)
    api_key = settings.VISUALCROSSING_API_KEY
    
    if not api_key:
        print("Error: VISUALCROSSING_API_KEY not found in .env file")
        print("\nPlease add to Backend/.env:")
        print('VISUALCROSSING_API_KEY="your_key_here"')
        sys.exit(1)
    
    # run backfill
    backfill_weather(
        api_key=api_key,
        calls_per_second=args.rate,
        year=args.year,
        dry_run=args.dry_run
    )


if __name__ == '__main__':
    main()
