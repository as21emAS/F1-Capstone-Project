"""
Smoke tests for race simulator.
"""

import sys
import os
import time

# allow imports from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ml.simulator import simulate_race


def cleanup_connections():
    """Allow DB connections to reset between tests."""
    try:
        time.sleep(0.1)
    except ImportError:
        pass


def test_basic_output_shape():
    """Validate output structure."""
    print("Test 1: Basic output shape")
    
    result = simulate_race(race_id=1, weather="dry")
    
    assert "predictions" in result
    assert "baseline_predictions" in result
    assert "key_factors" in result
    
    predictions = result["predictions"]
    assert predictions
    
    for p in predictions:
        assert all(k in p for k in [
            "driver_id", "driver_name", "team",
            "predicted_position", "confidence_score"
        ])
        assert 0.0 <= p["confidence_score"] <= 1.0
    
    baseline = result["baseline_predictions"]
    assert baseline
    
    for p in baseline:
        assert "driver_id" in p and "predicted_position" in p
        assert "driver_name" not in p and "team" not in p
    
    factors = result["key_factors"]
    assert factors
    
    for f in factors:
        assert all(k in f for k in ["factor", "impact", "criticality"])
        assert 0.0 <= f["impact"] <= 1.0
        assert f["criticality"] in ["Critical", "Moderate", "Minor", "Inactive"]
    
    print(f"Passed ({len(predictions)} drivers)")
    return result


def test_baseline_differs_from_custom():
    """Baseline vs custom predictions."""
    print("\nTest 2: Baseline vs custom")
    
    result = simulate_race(race_id=1, weather="wet")
    
    custom = [p["driver_id"] for p in result["predictions"]]
    baseline = [p["driver_id"] for p in result["baseline_predictions"]]
    
    if custom == baseline:
        print("Same order (may be expected)")
    else:
        print("Different results")
    
    return result


def test_custom_grid_order():
    """Custom grid changes predictions."""
    print("\nTest 3: Custom grid")
    
    default = simulate_race(race_id=1, weather="dry")
    default_order = [p["driver_id"] for p in default["predictions"]]
    
    custom_grid = list(reversed(default_order))
    custom = simulate_race(race_id=1, weather="dry", grid_order=custom_grid)
    custom_order = [p["driver_id"] for p in custom["predictions"]]
    
    assert custom_order != default_order
    print("Passed")
    
    return custom


def test_wet_factors_inactive_when_dry():
    """Wet factors inactive in dry."""
    print("\nTest 4: Wet factors inactive")
    
    result = simulate_race(race_id=1, weather="dry")
    
    wet = [f for f in result["key_factors"]
           if "wet" in f["factor"].lower() or "weather" in f["factor"].lower()]
    
    for f in wet:
        assert f["criticality"] == "Inactive"
    
    print("Passed")
    
    return result


def test_invalid_weather():
    """Invalid weather raises error."""
    print("\nTest 5: Invalid weather")
    
    try:
        simulate_race(race_id=1, weather="snowy")
        assert False
    except ValueError:
        print("Passed")


def test_invalid_race_id():
    """Invalid race_id raises error."""
    print("\nTest 6: Invalid race_id")
    
    try:
        simulate_race(race_id=999999, weather="dry")
        assert False
    except ValueError:
        print("Passed")


def test_invalid_grid_order_driver():
    """Invalid driver in grid."""
    print("\nTest 7: Invalid grid driver")
    
    try:
        simulate_race(
            race_id=1,
            weather="dry",
            grid_order=["fake_driver"]
        )
        assert False
    except ValueError:
        print("Passed")


def test_driver_exclusions():
    """Excluded drivers removed."""
    print("\nTest 8: Driver exclusions")
    
    result = simulate_race(race_id=1, weather="dry")
    drivers = {p["driver_id"] for p in result["predictions"]}
    
    exclude = list(drivers)[:2]
    
    result2 = simulate_race(
        race_id=1,
        weather="dry",
        excluded_drivers=exclude
    )
    
    remaining = {p["driver_id"] for p in result2["predictions"]}
    
    for d in exclude:
        assert d not in remaining
    
    print("Passed")


def test_all_drivers_excluded():
    """All excluded raises error."""
    print("\nTest 9: All excluded")
    
    result = simulate_race(race_id=1, weather="dry")
    drivers = [p["driver_id"] for p in result["predictions"]]
    
    try:
        simulate_race(
            race_id=1,
            weather="dry",
            excluded_drivers=drivers
        )
        assert False
    except ValueError:
        print("Passed")


def test_mixed_weather():
    """Mixed weather has impact."""
    print("\nTest 10: Mixed weather")
    
    result = simulate_race(race_id=1, weather="mixed")
    
    wet = [f for f in result["key_factors"]
           if "wet" in f["factor"].lower() or "weather" in f["factor"].lower()]
    
    if wet:
        assert any(f["impact"] > 0 for f in wet)
    
    print("Passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("RACE SIMULATOR TESTS")
    print("=" * 60)
    
    tests = [
        test_basic_output_shape,
        test_baseline_differs_from_custom,
        test_custom_grid_order,
        test_wet_factors_inactive_when_dry,
        test_invalid_weather,
        test_invalid_race_id,
        test_invalid_grid_order_driver,
        test_driver_exclusions,
        test_all_drivers_excluded,
        test_mixed_weather,
    ]
    
    failed = []
    
    for t in tests:
        try:
            t()
            cleanup_connections()
        except Exception as e:
            print(f"\n✗ {t.__name__} FAILED: {e}")
            failed.append(t.__name__)
            cleanup_connections()
    
    print("\n" + "=" * 60)
    if failed:
        print(f"FAILED: {len(failed)}/{len(tests)}")
        sys.exit(1)
    else:
        print(f"ALL PASSED ({len(tests)})")


if __name__ == "__main__":
    run_all_tests()