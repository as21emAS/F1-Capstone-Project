"""
Quick test for the simulator API endpoint
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_simulator_health():
    """Test simulator health endpoint"""
    print("Testing GET /api/simulator/health...")
    response = requests.get(f"{BASE_URL}/api/simulator/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 200


def test_basic_simulation():
    """Test basic simulation with dry weather"""
    print("Testing POST /api/simulator/simulate (dry weather)...")
    
    payload = {
        "race_id": 1,
        "weather": "dry"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/simulator/simulate",
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Predictions: {len(data['predictions'])} drivers")
        print(f"Baseline: {len(data['baseline_predictions'])} drivers")
        print(f"Key Factors: {len(data['key_factors'])} factors")
        print(f"\nTop 3:")
        for p in data['predictions'][:3]:
            print(f"  {p['predicted_position']}. {p['driver_name']} ({p['team']}) - {p['confidence_score']:.2%}")
        return True
    else:
        try:
            print(f"Error: {response.json()}")
        except:
            print(f"Error: {response.text}")
        return False


def test_custom_simulation():
    """Test simulation with custom weather and exclusions"""
    print("\nTesting POST /api/simulator/simulate (wet weather + exclusions)...")
    
    payload = {
        "race_id": 1,
        "weather": "wet",
        "excluded_drivers": ["webber", "alonso"]
    }
    
    response = requests.post(
        f"{BASE_URL}/api/simulator/simulate",
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Predictions: {len(data['predictions'])} drivers (2 excluded)")
        return True
    else:
        try:
            print(f"Error: {response.json()}")
        except:
            print(f"Error: {response.text}")
        return False


def test_invalid_input():
    """Test error handling"""
    print("\nTesting POST /api/simulator/simulate (invalid weather)...")
    
    payload = {
        "race_id": 1,
        "weather": "snowy"  # invalid
    }
    
    response = requests.post(
        f"{BASE_URL}/api/simulator/simulate",
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 400:
        print(f"Correctly rejected: {response.json()['detail']}")
        return True
    else:
        print(f"Expected 400, got {response.status_code}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("SIMULATOR API TESTS")
    print("=" * 60)
    print("Make sure the server is running: uvicorn app.main:app --reload\n")
    
    try:
        results = [
            test_simulator_health(),
            test_basic_simulation(),
            test_custom_simulation(),
            test_invalid_input()
        ]
        
        print("\n" + "=" * 60)
        passed = sum(results)
        total = len(results)
        print(f"RESULTS: {passed}/{total} tests passed")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\nERROR: Could not connect to API server")
        print("Make sure the server is running on http://localhost:8000")
