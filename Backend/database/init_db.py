#!/usr/bin/env python3
"""
Database initialization script for F1 Predictor
Creates tables, sets up indexes, and optionally loads initial data
"""

import os
import sys
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def run_sql_file(cursor, filepath):
    """Execute SQL from a file"""
    with open(filepath, 'r') as f:
        sql = f.read()
        cursor.execute(sql)
    print(f"✓ Executed {filepath}")

def initialize_database():
    """Initialize the database with schema and data"""
    
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        sys.exit(1)
    
    print("Initializing F1 Predictor database...")
    print(f"Database URL: {database_url}\n")
    
    try:
        # Connect to database
        conn = psycopg2.connect(database_url)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Run schema files
        print("Creating tables...")
        run_sql_file(cursor, 'Backend/database/schema/schema.sql')
        run_sql_file(cursor, 'Backend/database/schema/circuits_table.sql')
        run_sql_file(cursor, 'Backend/database/schema/additional_tables.sql')
        
        print("\nCreating indexes...")
        run_sql_file(cursor, 'Backend/database/schema/indexes.sql')
        
        print("\nAdding timestamps...")
        run_sql_file(cursor, 'Backend/database/schema/add_timestamps.sql')
        
        cursor.close()
        conn.close()
        
        print("\n✅ Database initialization complete!")
        print("\nNext steps:")
        print("  1. Run: python Backend/database/scripts/fetch_jolpica.py")
        print("     (This will populate historical race data)")
        
    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    initialize_database()
