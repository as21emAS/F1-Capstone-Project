"""
Visual Crossing Weather API Client
Fetches historical weather data for F1 race locations.
Free tier: 1,000 calls/day
"""

import requests
from typing import Dict, Optional
from datetime import datetime, date
import time
import json
import os


class RateLimiter:
    """Rate limiter for Visual Crossing API (1,000 calls/day free tier)"""
    
    def __init__(self, calls_per_second: float = 0.5):
        self.calls_per_second = calls_per_second
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0
    
    def wait(self):
        elapsed = time.time() - self.last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_call = time.time()


class CacheManager:    
    def __init__(self, cache_dir: str = ".cache/visualcrossing", ttl_days: int = 365):
        self.cache_dir = cache_dir
        self.ttl_seconds = ttl_days * 24 * 3600
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_path(self, key: str) -> str:
        """Generate cache file path from key"""
        safe_key = key.replace('/', '_').replace(':', '_').replace(',', '_')
        return os.path.join(self.cache_dir, f"{safe_key}.json")
    
    def get(self, key: str) -> Optional[Dict]:
        """Retrieve cached data if not expired"""
        cache_path = self._get_cache_path(key)
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, 'r') as f:
                cached = json.load(f)
            
            cached_time = datetime.fromisoformat(cached['timestamp'])
            if (datetime.now() - cached_time).total_seconds() > self.ttl_seconds:
                return None
            
            return cached['data']
        except (json.JSONDecodeError, KeyError, ValueError):
            return None
    
    def set(self, key: str, data: Dict):
        """Store data in cache with timestamp"""
        cache_path = self._get_cache_path(key)
        
        cached = {
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        
        with open(cache_path, 'w') as f:
            json.dump(cached, f)


class VisualCrossingClient:
    """
    Client for Visual Crossing Weather API
    """
    
    BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
    
    def __init__(self, api_key: str, calls_per_second: float = 0.5, cache_days: int = 365):
        if not api_key:
            raise ValueError("Visual Crossing API key is required")
        
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'F1-Predictor-App/1.0'
        })
        
        self.rate_limiter = RateLimiter(calls_per_second=calls_per_second)
        self.cache = CacheManager(ttl_days=cache_days)
    
    def _make_request(self, lat: float, lon: float, date_str: str, use_cache: bool = True) -> Optional[Dict]:
        """
        Make API request with rate limiting and caching
        
        Args:
            lat: Latitude
            lon: Longitude
            date_str: Date in YYYY-MM-DD format
            use_cache: Whether to use cached data
            
        Returns:
            API response data or None on error
        """
        # create cache key
        cache_key = f"{lat}_{lon}_{date_str}"
        
        # check cache first
        if use_cache:
            cached_data = self.cache.get(cache_key)
            if cached_data:
                print(f"Cache hit: {date_str} at ({lat}, {lon})")
                return cached_data
        
        # build URL
        url = f"{self.BASE_URL}/{lat},{lon}/{date_str}"
        
        params = {
            'key': self.api_key,
            'unitGroup': 'metric',  # Celsius, km/h, etc.
            'include': 'days',       # only need daily summary
            'elements': 'datetime,temp,humidity,precip,windspeed,conditions'  # only needed fields
        }
        
        try:
            self.rate_limiter.wait()
            
            print(f"Fetching weather: {date_str} at ({lat}, {lon})")
            response = self.session.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if use_cache:
                    self.cache.set(cache_key, data)
                
                print(f"Weather data retrieved")
                return data
            
            elif response.status_code == 401:
                print(f"Invalid API key")
                return None
            
            elif response.status_code == 429:
                print(f"Rate limit exceeded")
                return None
            
            else:
                print(f"Error: Status {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print(f"Request timed out")
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
            
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def get_historical_weather(self, lat: float, lon: float, race_date: date) -> Optional[Dict]:
        """
        Get historical weather for a specific date and location
        
        Args:
            lat: Latitude
            lon: Longitude
            race_date: Date of the race
            
        Returns:
            Formatted weather data matching your database schema or None
        """
        date_str = race_date.strftime('%Y-%m-%d')
        
        data = self._make_request(lat, lon, date_str)
        
        if not data or 'days' not in data or len(data['days']) == 0:
            return None
        
        # extract daily weather
        day_data = data['days'][0]
        
        # transform to match our database schema
        return {
            'temperature': day_data.get('temp'),
            'humidity': day_data.get('humidity'),
            'conditions': day_data.get('conditions', 'Unknown'),
            'wind_speed': day_data.get('windspeed'),
            'rainfall': day_data.get('precip', 0.0),  # Precipitation in mm
            'forecast_time': datetime.combine(race_date, datetime.min.time())
        }
    
    def get_weather_summary(self, lat: float, lon: float, race_date: date) -> Optional[str]:
        """
        Get human-readable weather summary for a historical date
        
        Args:
            lat: Latitude
            lon: Longitude
            race_date: Date of the race
            
        Returns:
            Weather summary string or None
        """
        weather = self.get_historical_weather(lat, lon, race_date)
        
        if not weather:
            return None
        
        temp = weather['temperature']
        condition = weather['conditions']
        rain = weather['rainfall']
        
        if rain > 0:
            return f"{condition}, {temp}°C (Wet - {rain}mm rain)"
        else:
            return f"{condition}, {temp}°C"
