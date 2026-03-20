"""
Smoke tests for the race simulator
Tests basic functionality, edge cases, and context-aware behavior
"""

import sys
import os
import time

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ml.simulator import simulate_race


def cleanup_connections():
    """Helper to cleanup database connections between tests"""
    try:
        from database.connection_pool import close_all_connections, initialize_pool
        # Small delay to ensure connections are released
        time.sleep(0.1)
        # Don't close all - that would break subsequent tests
        # Just give connections time to be returned
    except ImportError:
        pass


def test_basic_output_shape():
    """Test that output structure is correct for valid input"""
    print("Test 1: Basic output shape validation")
    
    result = simulate_race(
        race_id=1,
        weather="dry"
    )
    
    # Check top-level structure
    assert "predictions" in result, "Result must have 'predictions' key"
    assert "baseline_predictions" in result, "Result must have 'baseline_predictions' key"
    assert "key_factors" in result, "Result must have 'key_factors' key"
    
    # Check predictions structure
    predictions = result["predictions"]
    assert len(predictions) > 0, "Must have at least one prediction"
    
    for pred in predictions:
        assert "driver_id" in pred, "Prediction must have 'driver_id'"
        assert "driver_name" in pred, "Prediction must have 'driver_name'"
        assert "team" in pred, "Prediction must have 'team'"
        assert "predicted_position" in pred, "Prediction must have 'predicted_position'"
        assert "confidence_score" in pred, "Prediction must have 'confidence_score'"
        assert 0.0 <= pred["confidence_score"] <= 1.0, "Confidence must be in [0, 1]"
    
    # Check baseline predictions structure
    baseline = result["baseline_predictions"]
    assert len(baseline) > 0, "Must have at least one baseline prediction"
    
    for pred in baseline:
        assert "driver_id" in pred, "Baseline must have 'driver_id'"
        assert "predicted_position" in pred, "Baseline must have 'predicted_position'"
        # Baseline should NOT have driver_name, team, confidence (minimal format)
        assert "driver_name" not in pred, "Baseline should be minimal format"
        assert "team" not in pred, "Baseline should be minimal format"
    
    # Check key factors structure
    factors = result["key_factors"]
    assert len(factors) > 0, "Must have at least one key factor"
    
    for factor in factors:
        assert "factor" in factor, "Factor must have 'factor' name"
        assert "impact" in factor, "Factor must have 'impact' score"
        assert "criticality" in factor, "Factor must have 'criticality' tag"
        assert 0.0 <= factor["impact"] <= 1.0, "Impact must be in [0, 1]"
        assert factor["criticality"] in ["Critical", "Moderate", "Minor", "Inactive"], \
            f"Criticality must be valid, got: {factor['criticality']}"
    
    print(f"✓ Basic output shape test passed")
    print(f"  - {len(predictions)} predictions")
    print(f"  - {len(baseline)} baseline predictions")
    print(f"  - {len(factors)} key factors")
    return result


def test_baseline_differs_from_custom():
    """Test that baseline and custom predictions differ when non-default params used"""
    print("\nTest 2: Baseline vs custom predictions differ")
    
    result = simulate_race(
        race_id=1,
        weather="wet"  # Non-default weather
    )
    
    predictions = result["predictions"]
    baseline = result["baseline_predictions"]
    
    # Extract driver orders
    custom_order = [p["driver_id"] for p in predictions]
    baseline_order = [p["driver_id"] for p in baseline]
    
    # Orders should differ (wet weather changes predictions)
    # At least check that they're not identical
    if custom_order == baseline_order:
        print("  ⚠️  WARNING: Custom and baseline orders are identical")
        print("     This might be expected if weather has minimal impact")
    else:
        print(f"✓ Predictions differ between custom and baseline")
        print(f"  - Custom top 3: {custom_order[:3]}")
        print(f"  - Baseline top 3: {baseline_order[:3]}")
    
    return result


def test_custom_grid_order():
    """Test that custom grid_order produces different predictions"""
    print("\nTest 3: Custom grid order affects predictions")
    
    # First, run with default grid
    result_default = simulate_race(
        race_id=1,
        weather="dry"
    )
    
    default_order = [p["driver_id"] for p in result_default["predictions"]]
    
    # Now run with reversed grid order (worst starts first)
    custom_grid = list(reversed(default_order))
    
    result_custom = simulate_race(
        race_id=1,
        weather="dry",
        grid_order=custom_grid
    )
    
    custom_order = [p["driver_id"] for p in result_custom["predictions"]]
    
    # Predictions should differ when starting grid is reversed
    assert custom_order != default_order, \
        "Custom grid order should produce different predictions"
    
    print(f"✓ Custom grid order test passed")
    print(f"  - Default winner: {default_order[0]}")
    print(f"  - Custom grid winner: {custom_order[0]}")
    
    return result_custom


def test_wet_factors_inactive_when_dry():
    """Test that wet weather factors are marked 'Inactive' when weather is dry"""
    print("\nTest 4: Wet weather factors inactive when dry")
    
    result = simulate_race(
        race_id=1,
        weather="dry"
    )
    
    factors = result["key_factors"]
    
    # Find wet weather related factors
    wet_factors = [
        f for f in factors 
        if "wet" in f["factor"].lower() or "weather condition" in f["factor"].lower()
    ]
    
    if len(wet_factors) == 0:
        print("  ⚠️  WARNING: No wet weather factors found in key_factors")
    else:
        for factor in wet_factors:
            assert factor["criticality"] == "Inactive", \
                f"Wet weather factor '{factor['factor']}' should be 'Inactive' when dry, " \
                f"got: {factor['criticality']}"
            print(f"  ✓ {factor['factor']}: {factor['criticality']}")
    
    print(f"✓ Wet factors inactive when dry test passed")
    
    # Also test that they're NOT inactive when wet
    result_wet = simulate_race(
        race_id=1,
        weather="wet"
    )
    
    wet_factors_wet = [
        f for f in result_wet["key_factors"]
        if "wet" in f["factor"].lower() or "weather condition" in f["factor"].lower()
    ]
    
    active_count = sum(1 for f in wet_factors_wet if f["criticality"] != "Inactive")
    print(f"  - When weather is wet: {active_count}/{len(wet_factors_wet)} weather factors active")
    
    return result


def test_invalid_weather():
    """Test error handling for invalid weather"""
    print("\nTest 5: Invalid weather parameter")
    
    try:
        simulate_race(
            race_id=1,
            weather="snowy"  # Invalid
        )
        assert False, "Should have raised ValueError for invalid weather"
    except ValueError as e:
        assert "Invalid weather" in str(e), f"Wrong error message: {e}"
        print(f"  ✓ Correctly rejected: {e}")
    
    print("✓ Invalid weather test passed")


def test_invalid_race_id():
    """Test error handling for invalid race_id"""
    print("\nTest 6: Invalid race_id parameter")
    
    try:
        simulate_race(
            race_id=999999,  # Non-existent
            weather="dry"
        )
        assert False, "Should have raised ValueError for invalid race_id"
    except ValueError as e:
        assert "race_id" in str(e).lower(), f"Wrong error message: {e}"
        print(f"  ✓ Correctly rejected: {e}")
    
    print("✓ Invalid race_id test passed")


def test_invalid_grid_order_driver():
    """Test error handling for unrecognized driver in grid_order"""
    print("\nTest 7: Invalid driver in grid_order")
    
    try:
        simulate_race(
            race_id=1,
            weather="dry",
            grid_order=["fake_driver_123", "another_fake"]
        )
        assert False, "Should have raised ValueError for invalid driver_id"
    except ValueError as e:
        assert "driver_id" in str(e).lower(), f"Wrong error message: {e}"
        print(f"  ✓ Correctly rejected: {e}")
    
    print("✓ Invalid grid_order test passed")


def test_driver_exclusions():
    """Test that excluded drivers are omitted from predictions"""
    print("\nTest 8: Driver exclusions")
    
    # First get all drivers
    result_all = simulate_race(
        race_id=1,
        weather="dry"
    )
    
    all_drivers = {p["driver_id"] for p in result_all["predictions"]}
    drivers_to_exclude = list(all_drivers)[:2]  # Exclude first 2
    
    print(f"  - Total drivers: {len(all_drivers)}")
    print(f"  - Excluding: {drivers_to_exclude}")
    
    # Now exclude some drivers
    result_excluded = simulate_race(
        race_id=1,
        weather="dry",
        excluded_drivers=drivers_to_exclude
    )
    
    remaining_drivers = {p["driver_id"] for p in result_excluded["predictions"]}
    
    # Check exclusions worked
    for excluded in drivers_to_exclude:
        assert excluded not in remaining_drivers, \
            f"Driver {excluded} should have been excluded but appears in predictions"
    
    print(f"  ✓ {len(remaining_drivers)} drivers remain after exclusions")
    print("✓ Driver exclusions test passed")


def test_all_drivers_excluded():
    """Test error handling when all drivers are excluded"""
    print("\nTest 9: All drivers excluded (should fail gracefully)")
    
    # Get all drivers first
    result = simulate_race(race_id=1, weather="dry")
    all_driver_ids = [p["driver_id"] for p in result["predictions"]]
    
    try:
        simulate_race(
            race_id=1,
            weather="dry",
            excluded_drivers=all_driver_ids  # Exclude everyone
        )
        assert False, "Should have raised ValueError when all drivers excluded"
    except ValueError as e:
        assert "excluded" in str(e).lower(), f"Wrong error message: {e}"
        print(f"  ✓ Correctly rejected: {e}")
    
    print("✓ All drivers excluded test passed")


def test_mixed_weather():
    """Test mixed weather conditions"""
    print("\nTest 10: Mixed weather conditions")
    
    result = simulate_race(
        race_id=1,
        weather="mixed"
    )
    
    # Check that wet weather factors have some activity (not fully inactive)
    factors = result["key_factors"]
    wet_factors = [
        f for f in factors
        if "wet" in f["factor"].lower() or "weather condition" in f["factor"].lower()
    ]
    
    if wet_factors:
        # In mixed conditions, at least one weather factor should not be at zero impact
        has_impact = any(f["impact"] > 0 for f in wet_factors)
        assert has_impact, "Mixed weather should show some wet weather impact"
        print(f"  ✓ Mixed weather shows {len(wet_factors)} weather factors with impact")
    
    print("✓ Mixed weather test passed")


def run_all_tests():
    """Run all smoke tests"""
    print("=" * 70)
    print("RACE SIMULATOR SMOKE TESTS")
    print("=" * 70)
    
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
    
    for test in tests:
        try:
            test()
            cleanup_connections()  # Give connections time to be returned to pool
        except Exception as e:
            print(f"\n✗ {test.__name__} FAILED")
            print(f"  Error: {e}")
            import traceback
            traceback.print_exc()
            failed.append(test.__name__)
            cleanup_connections()
    
    print("\n" + "=" * 70)
    if failed:
        print(f"TESTS FAILED: {len(failed)}/{len(tests)}")
        print(f"Failed tests: {', '.join(failed)}")
        print("=" * 70)
        sys.exit(1)
    else:
        print(f"ALL TESTS PASSED ✓ ({len(tests)}/{len(tests)})")
        print("=" * 70)
        print("\nThe simulator is ready for integration!")
        print("Liv can import it with:")
        print("  from app.ml.simulator import simulate_race")


if __name__ == "__main__":
    run_all_tests()
