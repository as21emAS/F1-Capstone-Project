import requests
from typing import Dict, List, Optional
import time
from datetime import datetime, timedelta
import json
import os

#simple rate limiter to prevent API abuse
class RateLimiter:
    
    def __init__(self, calls_per_second: float = 2.0):
        self.calls_per_second = calls_per_second
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0
    
    #wait if necessary to respect rate limit
    def wait(self):
        elapsed = time.time() - self.last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_call = time.time()

#file-based cache for API responses
class CacheManager:
    
    def __init__(self, cache_dir: str = ".cache", ttl_hours: int = 6):
        self.cache_dir = cache_dir
        self.ttl = timedelta(hours=ttl_hours)
        os.makedirs(cache_dir, exist_ok=True)
    
    #Generate cache file path from key
    #Replace slashes to avoid path issues
    def _get_cache_path(self, key: str) -> str:
        safe_key = key.replace('/', '_')
        return os.path.join(self.cache_dir, f"{safe_key}.json")
    
    def get(self, key: str) -> Optional[Dict]:
        cache_path = self._get_cache_path(key)
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, 'r') as f:
                cached = json.load(f)
            
            cached_time = datetime.fromisoformat(cached['timestamp'])
            if datetime.now() - cached_time > self.ttl:
                return None
            
            return cached['data']
        except (json.JSONDecodeError, KeyError, ValueError):
            return None
    
    def set(self, key: str, data: Dict):
        cache_path = self._get_cache_path(key)
        
        cached = {
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        
        with open(cache_path, 'w') as f:
            json.dump(cached, f)
    
    #Clear all cached data
    def clear(self):
        if os.path.exists(self.cache_dir):
            for file in os.listdir(self.cache_dir):
                os.remove(os.path.join(self.cache_dir, file))

#Client for interacting with Jolpica F1 API
class JolpicaF1Client:    
    BASE_URL = "https://api.jolpi.ca/ergast/f1"
    
    def __init__(self, cache_hours: int = 6, calls_per_second: float = 2.0):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'F1-Predictor-App/1.0'
        })
        
        self.rate_limiter = RateLimiter(calls_per_second)
        self.cache = CacheManager(ttl_hours=cache_hours)
    
    def _make_request(self, endpoint: str, use_cache: bool = True, max_retries: int = 3) -> Optional[Dict]:
        
        #Check cache first
        if use_cache:
            cached_data = self.cache.get(endpoint)
            if cached_data:
                print(f"Cache hit: {endpoint}")
                return cached_data
        
        url = f"{self.BASE_URL}/{endpoint}"
        
        #Retry loop with exponential backoff
        for attempt in range(max_retries):
            try:
                self.rate_limiter.wait()
                
                print(f"Calling: {url} (attempt {attempt + 1}/{max_retries})")
                response = self.session.get(url, timeout=10)

                if response.status_code == 200:
                    print(f"Success! Status: {response.status_code}")
                    data = response.json()

                    if use_cache:
                        self.cache.set(endpoint, data)
                    
                    return data
                    
                elif response.status_code == 429:
                    
                    wait_time = 2 ** attempt
                    print(f"X Rate limited (429). Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    continue
                    
                elif response.status_code >= 500:
                    # Server error - retry
                    wait_time = 2 ** attempt
                    print(f"X Server error ({response.status_code}). Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                    
                else:
                    print(f"X Error: Status {response.status_code}")
                    return None
                    
            except requests.exceptions.Timeout:
                print(f"X Request timed out (attempt {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                return None
                
            except requests.exceptions.RequestException as e:
                print(f"X Request failed: {e} (attempt {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                return None
                
            except Exception as e:
                print(f"X Unexpected error: {e}")
                return None
        
        print(f"X All {max_retries} attempts failed")
        return None
    
    #Core API methods

    #get all races from the current season
    def get_current_season(self) -> List[Dict]:
        data = self._make_request("current.json")
        
        if data and 'MRData' in data:
            return data['MRData']['RaceTable']['Races']
        return []
    
    #Get race schedule for a specific season
    def get_race_schedule(self, season: int) -> List[Dict]:
        data = self._make_request(f"{season}.json")
        
        if data and 'MRData' in data:
            return data['MRData']['RaceTable']['Races']
        return []
    
    #Get info for the next race
    def get_next_race(self) -> Optional[Dict]:
        data = self._make_request("current/next.json")
        
        if data and 'MRData' in data:
            races = data['MRData']['RaceTable']['Races']
            if races:
                return races[0]
        return None
    
    #get results for specifi race
    def get_race_results(self, season: int, round_number: int) -> List[Dict]:
        data = self._make_request(f"{season}/{round_number}/results.json")
        
        if data and 'MRData' in data:
            races = data['MRData']['RaceTable']['Races']
            if races:
                return races[0]['Results']
        return []

    #Get driver championship standings
    def get_driver_standings(self, year: int = None) -> List[Dict]:
        
        endpoint = f"{year}/driverStandings.json" if year else "current/driverStandings.json"
        data = self._make_request(endpoint)
        
        if data and 'MRData' in data:
            standings_lists = data['MRData']['StandingsTable']['StandingsLists']
            if standings_lists:
                return standings_lists[0]['DriverStandings']
        return []

    #Get constructor (team) championship standings    
    def get_constructor_standings(self, year: int = None) -> List[Dict]:

        endpoint = f"{year}/constructorStandings.json" if year else "current/constructorStandings.json"
        data = self._make_request(endpoint)
        
        if data and 'MRData' in data:
            standings_lists = data['MRData']['StandingsTable']['StandingsLists']
            if standings_lists:
                return standings_lists[0]['ConstructorStandings']
        return []
    
    #Get qualifying results for a specific race
    def get_qualifying_results(self, year: int, round_number: int) -> List[Dict]:

        data = self._make_request(f"{year}/{round_number}/qualifying.json")
        
        if data and 'MRData' in data:
            races = data['MRData']['RaceTable']['Races']
            if races:
                return races[0].get('QualifyingResults', [])
        return []
    
    #Get information about all F1 circuits    
    def get_all_circuits(self) -> List[Dict]:

        data = self._make_request("circuits.json")
        
        if data and 'MRData' in data:
            return data['MRData']['CircuitTable']['Circuits']
        return []
    
    # Get all drivers for a season
    def get_all_drivers(self, year: int = None) -> List[Dict]:
        
        endpoint = f"{year}/drivers.json" if year else "current/drivers.json"
        data = self._make_request(endpoint)
        
        if data and 'MRData' in data:
            return data['MRData']['DriverTable']['Drivers']
        return []
    
    #Get all constructors (teams) for a season
    def get_all_constructors(self, year: int = None) -> List[Dict]:

        endpoint = f"{year}/constructors.json" if year else "current/constructors.json"
        data = self._make_request(endpoint)
        
        if data and 'MRData' in data:
            return data['MRData']['ConstructorTable']['Constructors']
        return []

    def clear_cache(self):
        # Clear all cached API responses
        self.cache.clear()
        print("Cache cleared")
