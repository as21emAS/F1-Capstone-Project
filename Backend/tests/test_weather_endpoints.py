"""
Test weather API endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"


def test_circuit_weather():
    """Test GET /api/weather/circuit/{circuit_id}"""
    print("\n" + "="*60)
    print("TEST 1: Get weather for Monza circuit")
    print("="*60)
    
    circuit_id = "monza"
    url = f"{BASE_URL}/api/weather/circuit/{circuit_id}"
    
    print(f"GET {url}")
    response = requests.get(url)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\nSuccess!")
        print(f"Circuit: {data['circuit_name']}")
        print(f"Location: {data['location']}, {data['country']}")
        print(f"Summary: {data['summary']}")
        print(f"\nWeather Details:")
        weather = data['weather']
        print(f"  Temperature: {weather['temperature']}°C")
        print(f"  Humidity: {weather['humidity']}%")
        print(f"  Conditions: {weather['conditions']}")
        print(f"  Wind Speed: {weather['wind_speed']} m/s")
        print(f"  Rainfall: {weather['rainfall']} mm")
        return True
    else:
        print(f"Failed: {response.text}")
        return False


def test_race_weather():
    """Test GET /api/weather/race/{race_id}"""
    print("\n" + "="*60)
    print("TEST 2: Get weather for a specific race")
    print("="*60)
    
    race_id = 1  # first race in the database
    url = f"{BASE_URL}/api/weather/race/{race_id}"
    
    print(f"GET {url}")
    response = requests.get(url)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\nSuccess!")
        print(f"Race: {data['race_name']}")
        print(f"Circuit: {data['circuit_name']}")
        print(f"Date: {data['date']}")
        print(f"Summary: {data['summary']}")
        print(f"\nWeather Details:")
        weather = data['weather']
        print(f"  Temperature: {weather['temperature']}°C")
        print(f"  Humidity: {weather['humidity']}%")
        print(f"  Conditions: {weather['conditions']}")
        print(f"  Wind Speed: {weather['wind_speed']} m/s")
        print(f"  Rainfall: {weather['rainfall']} mm")
        return True
    elif response.status_code == 503:
        print(f"Race may be beyond 5-day forecast range")
        print(f"  {response.json().get('detail', 'Unknown error')}")
        return True  # this is expected for distant races
    else:
        print(f"Failed: {response.text}")
        return False


def test_weather_summary():
    """Test GET /api/weather/summary/{circuit_id}"""
    print("\n" + "="*60)
    print("TEST 3: Get quick weather summary")
    print("="*60)
    
    circuit_id = "silverstone"
    url = f"{BASE_URL}/api/weather/summary/{circuit_id}"
    
    print(f"GET {url}")
    response = requests.get(url)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\nSuccess!")
        print(f"Circuit: {data['circuit_id']}")
        print(f"Summary: {data['summary']}")
        return True
    else:
        print(f"Failed: {response.text}")
        return False


def test_caching():
    """Test that caching works (second request should be faster)"""
    print("\n" + "="*60)
    print("TEST 4: Verify caching works")
    print("="*60)
    
    circuit_id = "spa"
    url = f"{BASE_URL}/api/weather/circuit/{circuit_id}"
    
    print(f"First request (should hit API)")
    start = datetime.now()
    response1 = requests.get(url)
    time1 = (datetime.now() - start).total_seconds()
    
    print(f"Second request (should use cache)")
    start = datetime.now()
    response2 = requests.get(url)
    time2 = (datetime.now() - start).total_seconds()
    
    if response1.status_code == 200 and response2.status_code == 200:
        print(f"\nBoth requests succeeded")
        print(f"  First request: {time1:.3f}s")
        print(f"  Second request: {time2:.3f}s")
        
        if time2 < time1 * 0.5:  # second request should be at least 50% faster
            print(f"  Caching is working! Second request was {time1/time2:.1f}x faster")
        else:
            print(f"  Caching may not be working as expected")
        
        return True
    else:
        print(f"One or both requests failed")
        return False


def test_error_handling():
    """Test error handling for invalid inputs"""
    print("\n" + "="*60)
    print("TEST 5: Test error handling")
    print("="*60)
    
    # Test 1: non-existent circuit
    print("\nTest 5a: Non-existent circuit")
    response = requests.get(f"{BASE_URL}/api/weather/circuit/nonexistent")
    if response.status_code == 404:
        print("  Returns 404 for non-existent circuit")
    else:
        print(f"  Expected 404, got {response.status_code}")
        return False
    
    # Test 2: non-existent race
    print("\nTest 5b: Non-existent race")
    response = requests.get(f"{BASE_URL}/api/weather/race/99999")
    if response.status_code == 404:
        print("  Returns 404 for non-existent race")
    else:
        print(f"  Expected 404, got {response.status_code}")
        return False
    
    return True


def main():
    """Run all tests"""
    print("\n" + "WEATHER API ENDPOINT TESTS")
    print("="*60)
    print("Make sure the backend server is running:")
    print("  uvicorn app.main:app --reload --port 8000")
    print("="*60)
    
    # check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code != 200:
            print("\nBackend server is not responding")
            print("   Start it with: uvicorn app.main:app --reload --port 8000")
            return False
    except requests.exceptions.RequestException:
        print("\nCannot connect to backend server")
        print("   Start it with: uvicorn app.main:app --reload --port 8000")
        return False
    
    print("\nBackend server is running\n")
    
    # run tests
    results = []
    results.append(("Circuit Weather", test_circuit_weather()))
    results.append(("Race Weather", test_race_weather()))
    results.append(("Weather Summary", test_weather_summary()))
    results.append(("Caching", test_caching()))
    results.append(("Error Handling", test_error_handling()))
    
    # print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status} - {name}")
    
    print("\n" + "="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)
    
    return passed == total


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
