from pydantic import BaseModel
from typing import List, Optional


class PredictionRequest(BaseModel):
    race_id: int
    weather: Optional[str] = None        # e.g. "dry", "wet", "mixed"
    tire_strategy: Optional[str] = None  # e.g. "soft", "medium", "hard"
    pit_stops: Optional[int] = None      # expected number of pit stops

    model_config = {
        "json_schema_extra": {
            "example": {
                "race_id": 1,
                "weather": "dry",
                "tire_strategy": "medium",
                "pit_stops": 2
            }
        }
    }


class DriverPrediction(BaseModel):
    position: int
    driver_id: str
    driver_name: str
    team: str
    confidence_score: float  # 0.0 - 1.0, win probability


class PredictionResponse(BaseModel):
    race_id: int
    model_version: str
    predictions: List[DriverPrediction]