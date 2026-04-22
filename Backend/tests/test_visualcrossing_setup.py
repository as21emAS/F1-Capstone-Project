"""
Quick test script to verify Visual Crossing API setup
Run this before doing the full backfill to ensure everything works.
"""

import os
import sys

# Add parent directory to path and change to Backend directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

from api_clients.visualcrossing_client import VisualCrossingClient
from app.core.config import settings
from datetime import date


def test_visual_crossing():
    """Test Visual Crossing client with a known race"""
    
    print("=" * 70)
    print("VISUAL CROSSING API TEST")
    print("=" * 70)
    print()
    
    # get API key from settings (automatically loads from .env)
    api_key = settings.VISUALCROSSING_API_KEY
    
    if not api_key:
        print("Error: VISUALCROSSING_API_KEY not found in .env file")
        print("\nPlease add to Backend/.env:")
        print('VISUALCROSSING_API_KEY="your_key_here"')
        return False
    
    print(f"✓ API key found: {api_key[:10]}...")
    print()
    
    # initialize client
    try:
        print("Initializing Visual Crossing client...")
        client = VisualCrossingClient(api_key=api_key, calls_per_second=1.0)
        print("Client initialized")
        print()
    except Exception as e:
        print(f"Failed to initialize client: {e}")
        return False
    
    # test with Monza 2024 (known race)
    print("Testing with Monza 2024 (September 1, 2024)...")
    print("Location: 45.6156°N, 9.2811°E")
    print()
    
    try:
        weather = client.get_historical_weather(
            lat=45.6156,
            lon=9.2811,
            race_date=date(2024, 9, 1)
        )
        
        if not weather:
            print("✗ No weather data returned")
            print("\nPossible issues:")
            print("- Invalid API key")
            print("- Rate limit exceeded")
            print("- Network error")
            return False
        
        print("Weather data retrieved successfully!")
        print()
        print("=" * 70)
        print("MONZA 2024 WEATHER:")
        print("=" * 70)
        print(f"Temperature:  {weather['temperature']}°C")
        print(f"Humidity:     {weather['humidity']}%")
        print(f"Wind Speed:   {weather['wind_speed']} km/h")
        print(f"Rainfall:     {weather['rainfall']} mm")
        print(f"Conditions:   {weather['conditions']}")
        print(f"Forecast Time: {weather['forecast_time']}")
        print("=" * 70)
        print()
        
        # test summary
        summary = client.get_weather_summary(
            lat=45.6156,
            lon=9.2811,
            race_date=date(2024, 9, 1)
        )
        print(f"Summary: {summary}")
        print()
        
        print("=" * 70)
        print("ALL TESTS PASSED")
        print("=" * 70)
        print("\nYou're ready to run the backfill script!")
        print("\nNext step:")
        print("  python scripts/backfill_historical_weather.py --dry-run")
        print()
        
        return True
        
    except Exception as e:
        print(f"Error fetching weather: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = test_visual_crossing()
    sys.exit(0 if success else 1)
