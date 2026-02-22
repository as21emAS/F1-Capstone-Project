import requests
from typing import Dict, List, Optional
import time

# Client for interacting with Jolpica F1 API
class JolpicaF1Client:
    BASE_URL = "https://api.jolpi.ca/ergast/f1"
    
    #Initialize the client
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'F1-Predictor-App/1.0'
        })
        self.rate_limit_delay = 0.5
    
    def _make_request(self, endpoint: str) -> Optional[Dict]:
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            print(f"Calling: {url}")
            response = self.session.get(url, timeout=10)
            
            # Check if successful
            if response.status_code == 200:
                print(f"Success! Status: {response.status_code}")
                data = response.json()
                time.sleep(self.rate_limit_delay)
                return data
            else:
                print(f"Error: Status {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return None
                
        except requests.exceptions.Timeout:
            print("Request timed out")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    #get information about the next upcoming race
    def get_next_race(self) -> Optional[Dict]:
        data = self._make_request("current/next.json")
        
        if data and 'MRData' in data:
            races = data['MRData']['RaceTable']['Races']
            if races:
                return races[0]
        return None
    
    #Get all races in the current season
    def get_current_season_races(self) -> List[Dict]:
        data = self._make_request("current.json")
        
        if data and 'MRData' in data:
            return data['MRData']['RaceTable']['Races']
        return []
    
    #get all races for a specific season
    def get_season_races(self, year: int) -> List[Dict]:
        data = self._make_request(f"{year}.json")
        
        if data and 'MRData' in data:
            return data['MRData']['RaceTable']['Races']
        return []
    
    #get driver standings for specific season
    def get_driver_standings(self, year: int = None) -> List[Dict]:
        endpoint = f"{year}/driverStandings.json" if year else "current/driverStandings.json"
        data = self._make_request(endpoint)
        
        if data and 'MRData' in data:
            standings_lists = data['MRData']['StandingsTable']['StandingsLists']
            if standings_lists:
                return standings_lists[0]['DriverStandings']
        return []
    
    #get constructor standings
    def get_constructor_standings(self, year: int = None) -> List[Dict]:
        endpoint = f"{year}/constructorStandings.json" if year else "current/constructorStandings.json"
        data = self._make_request(endpoint)
        
        if data and 'MRData' in data:
            standings_lists = data['MRData']['StandingsTable']['StandingsLists']
            if standings_lists:
                return standings_lists[0]['ConstructorStandings']
        return []
    
    #get results for specific race
    def get_race_results(self, year: int, round_number: int) -> List[Dict]:
        data = self._make_request(f"{year}/{round_number}/results.json")
        
        if data and 'MRData' in data:
            races = data['MRData']['RaceTable']['Races']
            if races:
                return races[0]['Results']
        return []
    
    #get qualifying results for specific race
    def get_qualifying_results(self, year: int, round_number: int) -> List[Dict]:

        data = self._make_request(f"{year}/{round_number}/qualifying.json")
        
        if data and 'MRData' in data:
            races = data['MRData']['RaceTable']['Races']
            if races:
                return races[0].get('QualifyingResults', [])
        return []
    
    #get all circuits
    def get_all_circuits(self) -> List[Dict]:
        data = self._make_request("circuits.json")
        
        if data and 'MRData' in data:
            return data['MRData']['CircuitTable']['Circuits']
        return []
    
    #get information about specific circuit
    def get_circuit_info(self, circuit_id: str) -> Optional[Dict]:
        data = self._make_request(f"circuits/{circuit_id}.json")
        
        if data and 'MRData' in data:
            circuits = data['MRData']['CircuitTable']['Circuits']
            if circuits:
                return circuits[0]
        return None
    
    #get all drivers for a season
    def get_all_drivers(self, year: int = None) -> List[Dict]:
        endpoint = f"{year}/drivers.json" if year else "current/drivers.json"
        data = self._make_request(endpoint)
        
        if data and 'MRData' in data:
            return data['MRData']['DriverTable']['Drivers']
        return []
    
    #get information about specific driver
    def get_driver_info(self, driver_id: str) -> Optional[Dict]:
        data = self._make_request(f"drivers/{driver_id}.json")
        
        if data and 'MRData' in data:
            drivers = data['MRData']['DriverTable']['Drivers']
            if drivers:
                return drivers[0]
        return None
    
    #get all constructors for a season
    def get_all_constructors(self, year: int = None) -> List[Dict]:
        endpoint = f"{year}/constructors.json" if year else "current/constructors.json"
        data = self._make_request(endpoint)
        
        if data and 'MRData' in data:
            return data['MRData']['ConstructorTable']['Constructors']
        return []
    
    #get information about specific constructor
    def get_constructor_info(self, constructor_id: str) -> Optional[Dict]:
        data = self._make_request(f"constructors/{constructor_id}.json")
        
        if data and 'MRData' in data:
            constructors = data['MRData']['ConstructorTable']['Constructors']
            if constructors:
                return constructors[0]
        return None
    
    #get lap times
    def get_lap_times(self, year: int, round_number: int, lap_number: int = None) -> List[Dict]:
        if lap_number:
            endpoint = f"{year}/{round_number}/laps/{lap_number}.json"
        else:
            endpoint = f"{year}/{round_number}/laps.json"
        
        data = self._make_request(endpoint)
        
        if data and 'MRData' in data:
            races = data['MRData']['RaceTable']['Races']
            if races and 'Laps' in races[0]:
                return races[0]['Laps']
        return []
    
    #get pit stop
    def get_pit_stops(self, year: int, round_number: int) -> List[Dict]:
        data = self._make_request(f"{year}/{round_number}/pitstops.json")
        
        if data and 'MRData' in data:
            races = data['MRData']['RaceTable']['Races']
            if races and 'PitStops' in races[0]:
                return races[0]['PitStops']
        return []

    def get_drivers_with_teams(self, year: int = 2024) -> List[Dict]:
        standings = self.get_driver_standings(year)
        drivers = []
    
        for entry in standings:
            driver_info = entry['Driver']
            constructor_info = entry['Constructors'][0] if entry.get('Constructors') else {}
        
            drivers.append({
                'driver_id': driver_info['driverId'],
                'driver_number': driver_info.get('permanentNumber'),
                'driver_code': driver_info.get('code'),
                'driver_forename': driver_info['givenName'],
                'driver_surname': driver_info['familyName'],
                'driver_full_name': f"{driver_info['givenName']} {driver_info['familyName']}",
                'nationality': driver_info.get('nationality'),
                'team_id': constructor_info.get('constructorId')
            })
    
        return drivers

#test function
#NOTE: Current standings are unavailable (2026 season hasn't started yet)
#So 2024 data will be used for testing purposes
if __name__ == "__main__":
    print("\n" + "="*70)
    print("TESTING JOLPICA F1 API CLIENT")
    print("="*70 + "\n")
    
    client = JolpicaF1Client()
    
    # Test 1: Get next race
    print("TEST 1: Getting next race...")
    next_race = client.get_next_race()
    if next_race:
        print(f"✅ Next Race: {next_race['raceName']}")
        print(f"   Circuit: {next_race['Circuit']['circuitName']}")
        print(f"   Location: {next_race['Circuit']['Location']['locality']}, {next_race['Circuit']['Location']['country']}")
        print(f"   Date: {next_race['date']}")
        print(f"   Time: {next_race.get('time', 'TBA')}\n")
    else:
        print("Error: No upcoming race found\n")
    
    # Test 2: Get driver standings (using 2024 season for testing)
    print("TEST 2: Getting 2024 driver standings...")
    standings = client.get_driver_standings(2024)
    if standings:
        print("✅ 2024 Championship Top 5:")
        for i, driver in enumerate(standings[:5], 1):
            driver_info = driver['Driver']
            name = f"{driver_info['givenName']} {driver_info['familyName']}"
            points = driver['points']
            wins = driver['wins']
            print(f"   {i}. {name:<25} {points} pts ({wins} wins)")
    else:
        print("Error: Failed to fetch driver standings")
    
    print()
    
    # Test 3: Get constructor standings (using 2024 seqason for testing)
    print("TEST 3: Getting 2024 constructor standings...")
    constructors = client.get_constructor_standings(2024)
    if constructors:
        print("✅ 2024 Constructor Top 5:")
        for i, team in enumerate(constructors[:5], 1):
            team_name = team['Constructor']['name']
            points = team['points']
            wins = team['wins']
            print(f"   {i}. {team_name:<25} {points} pts ({wins} wins)")
    else:
        print("Error: Failed to fetch constructor standings")
    
    print()
    
    # Test 4: Get 2024 season races
    print("TEST 4: Getting 2024 season calendar...")
    races_2024 = client.get_season_races(2024)
    if races_2024:
        print(f"✅ Found {len(races_2024)} races in 2024 season")
        print(f"   First: {races_2024[0]['raceName']}")
        print(f"   Last: {races_2024[-1]['raceName']}")
    else:
        print("Error: Failed to fetch 2024 calendar")
    
    print()
    
    # Test 5: Get all circuits
    print("TEST 5: Getting all circuits...")
    circuits = client.get_all_circuits()
    if circuits:
        print(f"✅ Found {len(circuits)} circuits in database")
        print(f"   Sample: {circuits[0]['circuitName']} ({circuits[0]['Location']['country']})")
    else:
        print("Error: Failed to fetch circuits")
    
    print()
    
    # Test 6: Get historical data (2023 Round 1 results)
    print("TEST 6: Getting 2023 Bahrain GP results (historical data test)...")
    results_2023 = client.get_race_results(2023, 1)
    if results_2023:
        print(f"✅ Found results for {len(results_2023)} drivers")
        winner = results_2023[0]
        print(f"   Winner: {winner['Driver']['givenName']} {winner['Driver']['familyName']}")
        print(f"   Team: {winner['Constructor']['name']}")
    else:
        print("Error: Failed to fetch 2023 results")
    
