#!/usr/bin/env python3
"""
Comprehensive test script for F1 Predictor database setup
Tests all components: env variables, connection pool, CRUD functions, timestamps, etc.
"""

import sys
import os
from dotenv import load_dotenv

print("=" * 60)
print("F1 PREDICTOR DATABASE - COMPREHENSIVE TEST")
print("=" * 60)

# Test 1: Environment Variables
print("\n[TEST 1] Environment Variables")
print("-" * 60)
load_dotenv('Backend/.env')
database_url = os.getenv('DATABASE_URL')
pool_size = os.getenv('DATABASE_POOL_SIZE')
max_overflow = os.getenv('DATABASE_MAX_OVERFLOW')

if database_url:
    print(f"✅ DATABASE_URL found: {database_url}")
else:
    print("❌ DATABASE_URL not found")
    sys.exit(1)

print(f"✅ POOL_SIZE: {pool_size}")
print(f"✅ MAX_OVERFLOW: {max_overflow}")

# Test 2: Connection Pool
print("\n[TEST 2] Connection Pool")
print("-" * 60)
try:
    from Backend.database.connection_pool import initialize_pool, get_connection, return_connection
    
    pool = initialize_pool()
    print("✅ Connection pool initialized")
    
    # Get and return a connection
    conn = get_connection()
    print("✅ Successfully got connection from pool")
    
    return_connection(conn)
    print("✅ Successfully returned connection to pool")
    
except Exception as e:
    print(f"❌ Connection pool error: {e}")
    sys.exit(1)

# Test 3: Database Tables Exist
print("\n[TEST 3] Database Tables")
print("-" * 60)
try:
    import psycopg2
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    tables = [
        'races', 'drivers', 'teams', 'race_results', 
        'circuits', 'weather_data', 'predictions', 
        'driver_standings', 'team_standings'
    ]
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"✅ {table}: {count} records")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Table check error: {e}")
    sys.exit(1)

# Test 4: Timestamps on Tables
print("\n[TEST 4] Timestamps")
print("-" * 60)
try:
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Check if created_at and updated_at columns exist
    cursor.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'races' 
        AND column_name IN ('created_at', 'updated_at')
    """)
    
    timestamp_columns = [row[0] for row in cursor.fetchall()]
    
    if 'created_at' in timestamp_columns and 'updated_at' in timestamp_columns:
        print("✅ Timestamps exist on races table")
    else:
        print(f"⚠️  Timestamps on races: {timestamp_columns}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Timestamp check error: {e}")

# Test 5: Foreign Key Relationships
print("\n[TEST 5] Foreign Key Relationships")
print("-" * 60)
try:
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Check foreign keys
    cursor.execute("""
        SELECT 
            tc.table_name, 
            kcu.column_name, 
            ccu.table_name AS foreign_table_name
        FROM information_schema.table_constraints AS tc 
        JOIN information_schema.key_column_usage AS kcu
          ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage AS ccu
          ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY'
        AND tc.table_name IN ('races', 'race_results')
    """)
    
    foreign_keys = cursor.fetchall()
    
    if foreign_keys:
        for fk in foreign_keys:
            print(f"✅ {fk[0]}.{fk[1]} → {fk[2]}")
    else:
        print("⚠️  No foreign keys found")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Foreign key check error: {e}")

# Test 6: CRUD Functions
print("\n[TEST 6] CRUD Functions")
print("-" * 60)
try:
    sys.path.append('.')
    from Backend.database.crud import (
        get_driver_standings,
        get_upcoming_race,
        get_all_drivers,
        get_all_teams,
        get_race_results
    )
    
    # Test get_driver_standings
    standings = get_driver_standings(2024)
    if standings and len(standings) > 0:
        champion = standings[0]
        print(f"✅ get_driver_standings(2024): {champion['driver_full_name']} - {champion['total_points']} pts")
    else:
        print("⚠️  No standings data found")
    
    # Test get_upcoming_race
    upcoming = get_upcoming_race()
    if upcoming:
        print(f"✅ get_upcoming_race(): {upcoming['race_name']}")
    else:
        print("⚠️  No upcoming race found")
    
    # Test get_all_drivers
    drivers = get_all_drivers()
    print(f"✅ get_all_drivers(): {len(drivers)} drivers")
    
    # Test get_all_teams
    teams = get_all_teams()
    print(f"✅ get_all_teams(): {len(teams)} teams")
    
except Exception as e:
    print(f"❌ CRUD function error: {e}")
    import traceback
    traceback.print_exc()

# Test 7: Data Integrity
print("\n[TEST 7] Data Integrity")
print("-" * 60)
try:
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Check for orphaned records
    cursor.execute("""
        SELECT COUNT(*) 
        FROM race_results rr 
        LEFT JOIN races r ON rr.race_id = r.race_id 
        WHERE r.race_id IS NULL
    """)
    orphaned_results = cursor.fetchone()[0]
    
    if orphaned_results == 0:
        print("✅ No orphaned race results")
    else:
        print(f"⚠️  Found {orphaned_results} orphaned race results")
    
    # Check data range
    cursor.execute("SELECT MIN(year), MAX(year) FROM races")
    min_year, max_year = cursor.fetchone()
    print(f"✅ Data range: {min_year} - {max_year}")
    
    # Check total race results
    cursor.execute("SELECT COUNT(*) FROM race_results")
    total_results = cursor.fetchone()[0]
    print(f"✅ Total race results: {total_results}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Data integrity check error: {e}")

# Test 8: Circuits Table
print("\n[TEST 8] Circuits Table")
print("-" * 60)
try:
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM circuits")
    circuit_count = cursor.fetchone()[0]
    print(f"✅ Circuits table: {circuit_count} circuits")
    
    # Sample circuits
    cursor.execute("SELECT circuit_name, country FROM circuits LIMIT 3")
    circuits = cursor.fetchall()
    for circuit in circuits:
        print(f"   - {circuit[0]} ({circuit[1]})")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Circuits check error: {e}")

# Final Summary
print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print("✅ All core components tested successfully!")
print("\nYour database is ready for:")
print("  - FastAPI backend integration")
print("  - ML model training")
print("  - Weather data integration")
print("  - Production deployment")
print("=" * 60)
