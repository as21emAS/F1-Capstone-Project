"""
OpenWeather API Client
Fetches current weather and forecasts for F1 race locations.
Free tier: 1,000 calls/day
"""

import requests
from typing import Dict, Optional
import time
from datetime import datetime, timedelta
import json
import os


class RateLimiter:    
    def __init__(self, calls_per_minute: int = 60):
        self.calls_per_minute = calls_per_minute
        self.min_interval = 60.0 / calls_per_minute
        self.last_call = 0
    
    def wait(self):
        elapsed = time.time() - self.last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_call = time.time()


class CacheManager:    
    def __init__(self, cache_dir: str = ".cache/weather", ttl_hours: int = 1):
        self.cache_dir = cache_dir
        self.ttl = timedelta(hours=ttl_hours)
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
            if datetime.now() - cached_time > self.ttl:
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


class OpenWeatherClient:
    """
    Client for OpenWeather API
    
    Supports:
    - Current weather conditions
    - 5-day forecast (3-hour intervals)
    - Weather at specific coordinates (circuit locations)
    """
    
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    def __init__(self, api_key: str, cache_hours: int = 1):
        if not api_key:
            raise ValueError("OpenWeather API key is required")
        
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'F1-Predictor-App/1.0'
        })
        
        self.rate_limiter = RateLimiter(calls_per_minute=60)
        self.cache = CacheManager(ttl_hours=cache_hours)
    
    def _make_request(self, endpoint: str, params: Dict, use_cache: bool = True) -> Optional[Dict]:
        # add API key to params
        params['appid'] = self.api_key
        params['units'] = 'metric'  # Use Celsius
        
        # create cache key
        cache_key = f"{endpoint}_{json.dumps(params, sort_keys=True)}"
        
        # check cache first
        if use_cache:
            cached_data = self.cache.get(cache_key)
            if cached_data:
                print(f"✓ Weather cache hit: {endpoint}")
                return cached_data
        
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            self.rate_limiter.wait()
            
            print(f"→ Calling OpenWeather API: {endpoint}")
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if use_cache:
                    self.cache.set(cache_key, data)
                
                print(f"✓ Weather data retrieved successfully")
                return data
            
            elif response.status_code == 401:
                print(f"✗ Invalid API key")
                return None
            
            elif response.status_code == 429:
                print(f"✗ Rate limit exceeded")
                return None
            
            else:
                print(f"✗ Error: Status {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print(f"✗ Request timed out")
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Request failed: {e}")
            return None
            
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            return None
    
    def get_current_weather(self, lat: float, lon: float) -> Optional[Dict]:
        """
        Get current weather at coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Formatted weather data or None
        """
        params = {
            'lat': lat,
            'lon': lon
        }
        
        data = self._make_request('weather', params)
        
        if not data:
            return None
        
        # transform to match our database schema
        return {
            'temperature': data.get('main', {}).get('temp'),
            'humidity': data.get('main', {}).get('humidity'),
            'conditions': data.get('weather', [{}])[0].get('description', 'Unknown'),
            'wind_speed': data.get('wind', {}).get('speed'),
            'rainfall': data.get('rain', {}).get('1h', 0.0),  # rain volume last hour
            'forecast_time': datetime.now()
        }
    
    def get_forecast(self, lat: float, lon: float, days: int = 5) -> Optional[list]:
        """
        Get weather forecast at coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
            days: Number of days (max 5 for free tier)
            
        Returns:
            List of forecast data points or None
        """
        params = {
            'lat': lat,
            'lon': lon,
            'cnt': min(days * 8, 40)  # 8 data points per day (3-hour intervals)
        }
        # make API request
        data = self._make_request('forecast', params)
        
        if not data or 'list' not in data:
            return None
        
        # transform forecast data
        forecasts = []
        for item in data['list']:
            forecasts.append({
                'temperature': item.get('main', {}).get('temp'),
                'humidity': item.get('main', {}).get('humidity'),
                'conditions': item.get('weather', [{}])[0].get('description', 'Unknown'),
                'wind_speed': item.get('wind', {}).get('speed'),
                'rainfall': item.get('rain', {}).get('3h', 0.0),  # rain volume last 3 hours
                'forecast_time': datetime.fromtimestamp(item.get('dt'))
            })
        
        return forecasts
    
    def get_race_weather(self, lat: float, lon: float, race_date: datetime) -> Optional[Dict]:
        """
        Get weather for a specific race date (current if today, forecast if future)
        
        Args:
            lat: Circuit latitude
            lon: Circuit longitude
            race_date: Date of the race
            
        Returns:
            Weather data or None
        """
        now = datetime.now()
        race_date_only = race_date.replace(hour=0, minute=0, second=0, microsecond=0)
        now_only = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        days_until_race = (race_date_only - now_only).days
        
        # if race is today or in the past, get current weather
        if days_until_race <= 0:
            return self.get_current_weather(lat, lon)
        
        # if race is more than 5 days away, we can't forecast (free tier limit)
        if days_until_race > 5:
            print(f"Race is {days_until_race} days away - beyond forecast range")
            return None
        
        # get forecast and find closest to race time
        forecasts = self.get_forecast(lat, lon, days=days_until_race + 1)
        
        if not forecasts:
            return None
        
        # find forecast closest to race time
        closest_forecast = min(
            forecasts,
            key=lambda f: abs((f['forecast_time'] - race_date).total_seconds())
        )
        
        return closest_forecast
    
    def get_weather_summary(self, lat: float, lon: float) -> Optional[str]:
        weather = self.get_current_weather(lat, lon)
        
        if not weather:
            return None
        
        temp = weather['temperature']
        condition = weather['conditions']
        rain = weather['rainfall']
        
        if rain > 0:
            return f"{condition.title()}, {temp}°C (Wet conditions)"
        else:
            return f"{condition.title()}, {temp}°C"
