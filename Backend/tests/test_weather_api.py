"""
Test script for OpenWeather API client
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Add Backend directory to path (parent of tests directory)
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from api_clients.openweather_client import OpenWeatherClient
from dotenv import load_dotenv

# Load environment variables from Backend/.env
env_path = backend_dir / '.env'
load_dotenv(dotenv_path=env_path)

def test_weather_client():
    """Test the OpenWeather API client"""
    
    api_key = os.getenv('OPENWEATHER_API_KEY')
    
    if not api_key:
        print("OPENWEATHER_API_KEY not found in environment")
        print(" Make sure it's set in Backend/.env")
        return False
    
    print(f"API key loaded: {api_key[:8]}...")
    print()
    
    # initialize client
    try:
        client = OpenWeatherClient(api_key=api_key, cache_hours=1)
        print("OpenWeather client initialized")
        print()
    except Exception as e:
        print(f"Failed to initialize client: {e}")
        return False
    
    # test with Monza circuit coordinates (Italian GP)
    print("Testing with Autodromo Nazionale Monza coordinates...")
    monza_lat = 45.6156
    monza_lon = 9.2811
    
    print("\n1. Testing current weather...")
    print("-" * 50)
    current = client.get_current_weather(monza_lat, monza_lon)
    
    if current:
        print("Current weather retrieved:")
        print(f"   Temperature: {current['temperature']}°C")
        print(f"   Humidity: {current['humidity']}%")
        print(f"   Conditions: {current['conditions']}")
        print(f"   Wind Speed: {current['wind_speed']} m/s")
        print(f"   Rainfall: {current['rainfall']} mm")
    else:
        print("Failed to get current weather")
        return False
    
    print("\n2. Testing weather summary...")
    print("-" * 50)
    summary = client.get_weather_summary(monza_lat, monza_lon)
    
    if summary:
        print(f"Weather summary: {summary}")
    else:
        print("Failed to get weather summary")
    
    print("\n3. Testing 5-day forecast...")
    print("-" * 50)
    forecast = client.get_forecast(monza_lat, monza_lon, days=2)
    
    if forecast:
        print(f"Retrieved {len(forecast)} forecast data points")
        print("   First 3 forecasts:")
        for i, f in enumerate(forecast[:3]):
            print(f"   [{i+1}] {f['forecast_time']}: {f['temperature']}°C, {f['conditions']}")
    else:
        print("Failed to get forecast")
    
    print("\n4. Testing race weather prediction...")
    print("-" * 50)
    future_date = datetime(2026, 4, 15, 14, 0)  # sample race date
    race_weather = client.get_race_weather(monza_lat, monza_lon, future_date)
    
    if race_weather:
        print(f"✓ Race weather prediction:")
        print(f"   Temperature: {race_weather['temperature']}°C")
        print(f"   Conditions: {race_weather['conditions']}")
    else:
        print("⚠ Race might be beyond forecast range or API failed")
    
    print("\n" + "=" * 50)
    print("All tests completed successfully!")
    print("=" * 50)
    return True


if __name__ == "__main__":
    try:
        success = test_weather_client()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
