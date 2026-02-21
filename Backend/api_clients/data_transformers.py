#Data transformation functions to convert API responses into database format

#Race info
def transform_race(race_data):
    circuit = race_data.get('Circuit', {})
    location = circuit.get('Location', {})
    
    return {
        'year': int(race_data.get('season', 0)),
        'round': int(race_data.get('round', 0)),
        'race_name': race_data.get('raceName', ''),
        'circuit_id': circuit.get('circuitId', ''),
        'circuit_name': circuit.get('circuitName', ''),
        'country': location.get('country', ''),
        'date': race_data.get('date', '')
    }

#Driver info
def transform_driver(driver_data):
    given = driver_data.get('givenName', '')
    family = driver_data.get('familyName', '')
    
    return {
        'driver_id': driver_data.get('driverId', ''),
        'driver_number': driver_data.get('permanentNumber'),
        'driver_code': driver_data.get('code'),
        'driver_forename': given,
        'driver_surname': family,
        'driver_full_name': f"{given} {family}"
    }

#Team info
def transform_team(team_data):
    return {
        'team_id': team_data.get('constructorId', ''),
        'team_name': team_data.get('name', '')
    }

#Race result info
def transform_result(result_data):
    driver = result_data.get('Driver', {})
    team = result_data.get('Constructor', {})
    status = result_data.get('status', '')
    position = result_data.get('position')
    
    #Check if DNF
    dnf_keywords = ['Retired', 'Accident', 'Collision', 'Engine', 'Gearbox']
    is_dnf = any(word in status for word in dnf_keywords)
    
    return {
        #Driver
        'driver_id': driver.get('driverId', ''),
        'driver_full_name': f"{driver.get('givenName', '')} {driver.get('familyName', '')}",
        
        #Team
        'team_id': team.get('constructorId', ''),
        'team_name': team.get('name', ''),
        
        #Result
        'grid_position': int(result_data.get('grid', 0)),
        'finish_position': int(position) if position else None,
        'position_text': result_data.get('positionText', ''),
        'points': float(result_data.get('points', 0)),
        'laps_completed': int(result_data.get('laps', 0)),
        'status': status,
        'time': result_data.get('Time', {}).get('time'),
        
        #Flags
        'finished': position is not None and not is_dnf,
        'dnf': is_dnf
    }


#Test
if __name__ == "__main__":
    from jolpica_f1_client import JolpicaF1Client
    
    print("\nTesting Data Transformers\n")
    
    client = JolpicaF1Client()
    
    #Testing race transformation
    races = client.get_season_races(2024)
    if races:
        transformed = transform_race(races[0])
        print("Race transformation works:")
        print(f"   {transformed['race_name']} - {transformed['date']}")
    
    #Testing result transformation
    results = client.get_race_results(2023, 1)
    if results:
        transformed = transform_result(results[0])
        print(f"\nResult transformation works:")
        print(f"   Winner: {transformed['driver_full_name']}")
        print(f"   Team: {transformed['team_name']}")
        print(f"   Points: {transformed['points']}")
    
    print("\nAll transformers working.\n")