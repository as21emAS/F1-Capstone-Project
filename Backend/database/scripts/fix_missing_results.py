import sys
sys.path.append('Backend/database/scripts')
from jolpica_f1_client import JolpicaF1Client
from transformers import transform_result, transform_driver, transform_team
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    return psycopg2.connect(
        dbname="f1_predictor",
        user="livreiter",
        password="",
        host="localhost",
        port="5432"
    )

def insert_driver(cursor, driver_data):
    cursor.execute("""
        INSERT INTO drivers (driver_id, driver_number, driver_code, driver_forename, driver_surname, driver_full_name)
        VALUES (%(driver_id)s, %(driver_number)s, %(driver_code)s, %(driver_forename)s, %(driver_surname)s, %(driver_full_name)s)
        ON CONFLICT (driver_id) DO UPDATE SET
            driver_number = EXCLUDED.driver_number,
            driver_code = EXCLUDED.driver_code
    """, driver_data)

def insert_team(cursor, team_data):
    cursor.execute("""
        INSERT INTO teams (team_id, team_name)
        VALUES (%(team_id)s, %(team_name)s)
        ON CONFLICT (team_id) DO UPDATE SET
            team_name = EXCLUDED.team_name
    """, team_data)

def insert_result(cursor, result_data, race_id):
    cursor.execute("""
        INSERT INTO race_results 
        (race_id, driver_id, team_id, grid_position, finish_position, position_text, 
         points, laps_completed, status, time, finished, dnf)
        VALUES (%(race_id)s, %(driver_id)s, %(team_id)s, %(grid_position)s, %(finish_position)s, 
                %(position_text)s, %(points)s, %(laps_completed)s, %(status)s, %(time)s, 
                %(finished)s, %(dnf)s)
        ON CONFLICT (race_id, driver_id) DO UPDATE SET
            finish_position = EXCLUDED.finish_position,
            points = EXCLUDED.points,
            status = EXCLUDED.status
    """, {**result_data, 'race_id': race_id})

print("Fixing missing race results...")
client = JolpicaF1Client()
conn = get_db_connection()
cursor = conn.cursor(cursor_factory=RealDictCursor)


cursor.execute("""
    SELECT r.race_id, r.year, r.round, r.race_name
    FROM races r
    LEFT JOIN race_results rr ON r.race_id = rr.race_id
    GROUP BY r.race_id
    HAVING COUNT(rr.result_id) = 0
    ORDER BY r.year, r.round
""")

races_without_results = cursor.fetchall()
print(f"Found {len(races_without_results)} races without results")

for race in races_without_results:
    year = race['year']
    round_num = race['round']
    race_id = race['race_id']
    
    print(f"  Fetching: {year} Round {round_num} - {race['race_name']}")
    
    try:
        results = client.get_race_results(year, round_num)
        
        if not results:
            print(f"    ⚠ No results available (future race or not run yet)")
            continue
        
        for result in results:
            result_data = transform_result(result)
            driver_data = transform_driver(result.get('Driver', {}))
            team_data = transform_team(result.get('Constructor', {}))
            
            insert_driver(cursor, driver_data)
            insert_team(cursor, team_data)
            insert_result(cursor, result_data, race_id)
        
        conn.commit()
        print(f"    ✓ Inserted {len(results)} results")
        
    except Exception as e:
        print(f"    ✗ Error: {e}")
        conn.rollback()

cursor.close()
conn.close()
print("\n✓ Done!")