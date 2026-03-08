from fastapi import APIRouter, HTTPException
from app.schemas.predictions import PredictionRequest, PredictionResponse, DriverPrediction
from app.ml.predictor import predictor

router = APIRouter()

# 2025 F1 driver roster — driver_id matches what the model was trained on
DRIVERS = [
    {"driver_id": "max_verstappen",     "driver_name": "Max Verstappen",     "team": "Red Bull Racing"},
    {"driver_id": "liam_lawson",        "driver_name": "Liam Lawson",        "team": "Red Bull Racing"},
    {"driver_id": "lando_norris",       "driver_name": "Lando Norris",       "team": "McLaren"},
    {"driver_id": "oscar_piastri",      "driver_name": "Oscar Piastri",      "team": "McLaren"},
    {"driver_id": "charles_leclerc",    "driver_name": "Charles Leclerc",    "team": "Ferrari"},
    {"driver_id": "lewis_hamilton",     "driver_name": "Lewis Hamilton",     "team": "Ferrari"},
    {"driver_id": "george_russell",     "driver_name": "George Russell",     "team": "Mercedes"},
    {"driver_id": "andrea_antonelli",   "driver_name": "Andrea Kimi Antonelli", "team": "Mercedes"},
    {"driver_id": "fernando_alonso",    "driver_name": "Fernando Alonso",    "team": "Aston Martin"},
    {"driver_id": "lance_stroll",       "driver_name": "Lance Stroll",       "team": "Aston Martin"},
    {"driver_id": "pierre_gasly",       "driver_name": "Pierre Gasly",       "team": "Alpine"},
    {"driver_id": "jack_doohan",        "driver_name": "Jack Doohan",        "team": "Alpine"},
    {"driver_id": "carlos_sainz",       "driver_name": "Carlos Sainz",       "team": "Williams"},
    {"driver_id": "alexander_albon",    "driver_name": "Alexander Albon",    "team": "Williams"},
    {"driver_id": "yuki_tsunoda",       "driver_name": "Yuki Tsunoda",       "team": "RB"},
    {"driver_id": "isack_hadjar",       "driver_name": "Isack Hadjar",       "team": "RB"},
    {"driver_id": "nico_hulkenberg",    "driver_name": "Nico Hulkenberg",    "team": "Sauber"},
    {"driver_id": "gabriel_bortoleto",  "driver_name": "Gabriel Bortoleto",  "team": "Sauber"},
    {"driver_id": "oliver_bearman",     "driver_name": "Oliver Bearman",     "team": "Haas"},
    {"driver_id": "esteban_ocon",       "driver_name": "Esteban Ocon",       "team": "Haas"},
]


@router.post("/", response_model=PredictionResponse)
def predict_race(request: PredictionRequest):
    """
    Predict race winner probabilities for all 2025 drivers.

    Runs the RandomForestClassifier once per driver and ranks them
    by win probability (confidence_score descending).
    """
    try:
        results = predictor.predict_race_winner(
            race_id=request.race_id,
            params={
                "weather": request.weather,
                "tire_strategy": request.tire_strategy,
                "pit_stops": request.pit_stops,
            }
        )

        # Map predictor output (driver_id + confidence) to full response
        result_map = {r["driver_id"]: r for r in results}

        predictions = []
        for driver in DRIVERS:
            driver_result = result_map.get(driver["driver_id"])
            confidence = driver_result["confidence_score"] if driver_result else 0.0
            predictions.append({
                "driver_id": driver["driver_id"],
                "driver_name": driver["driver_name"],
                "team": driver["team"],
                "confidence_score": round(confidence, 4),
            })

        # Sort by confidence descending and assign positions
        predictions.sort(key=lambda x: x["confidence_score"], reverse=True)
        ranked = [
            DriverPrediction(position=i + 1, **p)
            for i, p in enumerate(predictions)
        ]

        return PredictionResponse(
            race_id=request.race_id,
            model_version=predictor.get_model_info()["version"],
            predictions=ranked,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")