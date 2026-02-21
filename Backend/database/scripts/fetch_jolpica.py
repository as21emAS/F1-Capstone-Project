
from jolpica_f1_client import JolpicaF1Client
from transformers import transform_race, transform_driver, transform_team, transform_result
import psycopg2
from psycopg2.extras import execute_values

def get_db_connection():
    
    return psycopg2.connect(
        dbname="f1_predictor",
        user="livreiter",  
        password="",  
        host="localhost",
        port="5432"
    )

def insert_race(cursor, race_data):
  
    cursor.execute("""
        INSERT INTO races (year, round, race_name, circuit_id, circuit_name, country, date)
        VALUES (%(year)s, %(round)s, %(race_name)s, %(circuit_id)s, %(circuit_name)s, %(country)s, %(date)s)
        ON CONFLICT (year, round) DO NOTHING
        RETURNING race_id
    """, race_data)
    result = cursor.fetchone()
    return result[0] if result else None

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
        ON CONFLICT (race_id, driver_id) DO NOTHING
    """, {**result_data, 'race_id': race_id})

def fetch_season_data(year):
    
    client = JolpicaF1Client()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        print(f"Fetching data for {year} season...")
        
       
        races = client.get_season_races(year)
        
        for race in races:
           
            race_data = transform_race(race)
            race_id = insert_race(cursor, race_data)
            
            if not race_id:
              
                cursor.execute(
                    "SELECT race_id FROM races WHERE year = %s AND round = %s",
                    (race_data['year'], race_data['round'])
                )
                race_id = cursor.fetchone()[0]
            
            print(f"  Processing: {race_data['race_name']}")
            
           
            results = client.get_race_results(year, race_data['round'])
            
            for result in results:
               
                result_data = transform_result(result)
                
               
                driver_data = transform_driver(result.get('Driver', {}))
                team_data = transform_team(result.get('Constructor', {}))
                
                insert_driver(cursor, driver_data)
                insert_team(cursor, team_data)
                insert_result(cursor, result_data, race_id)
        
        conn.commit()
        print(f"✓ Successfully loaded {year} season data")
        
    except Exception as e:
        conn.rollback()
        print(f"✗ Error loading {year} data: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
   
    for year in range(2010, 2026):
        fetch_season_data(year)