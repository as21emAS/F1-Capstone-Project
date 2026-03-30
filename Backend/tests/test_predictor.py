"""
Smoke test for ML predictor
Tests that the model loads and the predict_race_winner function works
"""

import sys
from pathlib import Path

# add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.ml.predictor import predictor

def test_model_loads():
    """Test that model loads without errors"""
    print("Testing model load...")
    assert predictor.model is not None, "Model failed to load"
    print("Model loaded successfully")

def test_model_info():
    """Test that model info is accessible"""
    print("\nTesting model info...")
    info = predictor.get_model_info()
    print(f"Model version: {info['version']}")
    print(f"Model type: {info['model_type']}")
    print(f"Features ({len(info['features'])}): {info['features']}")

def test_predict_race_winner():
    """Test that predict_race_winner returns expected format"""
    print("\nTesting predict_race_winner...")
    
    # test with dummy race_id
    result = predictor.predict_race_winner(race_id=1)
    
    assert isinstance(result, list), "Result should be a list"
    assert len(result) > 0, "Result should not be empty"
    
    # check first prediction has required fields
    first = result[0]
    assert "driver_id" in first, "Missing driver_id"
    assert "predicted_position" in first, "Missing predicted_position"
    assert "confidence_score" in first, "Missing confidence_score"
    
    print(f"Function returns list of {len(result)} predictions")
    print(f"Sample prediction: {first}")

def main():
    print("="*60)
    print("F1 PREDICTOR SMOKE TEST")
    print("="*60)
    
    try:
        test_model_loads()
        test_model_info()
        test_predict_race_winner()
        
        print("\n" + "="*60)
        print("ALL TESTS PASSED")
        print("="*60)
        
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
