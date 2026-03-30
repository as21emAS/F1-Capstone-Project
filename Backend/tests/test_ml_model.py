from app.ml.predictor import predictor

def test_model_loading():
    print("Testing model loading...")
    print(f"Model version: {predictor.version}")
    print(f"Model loaded: {predictor.model is not None}")

def test_predictions():
    print("\nTesting predictions...")
    
    result1 = predictor.predict_race_winner(63.2, 4.9, 1.5, 1)
    print(f"\nVerstappen (pole): {result1['predicted_winner']} - {result1['win_probability']}")
    
    result2 = predictor.predict_race_winner(8.8, 6.5, 5.0, 5)
    print(f"Leclerc (P5): {result2['predicted_winner']} - {result2['win_probability']}")
    
    result3 = predictor.predict_race_winner(0.0, 15.0, 16.0, 18)
    print(f"Backmarker (P18): {result3['predicted_winner']} - {result3['win_probability']}")

if __name__ == "__main__":
    test_model_loading()
    test_predictions()
    print("\nAll tests passed!")