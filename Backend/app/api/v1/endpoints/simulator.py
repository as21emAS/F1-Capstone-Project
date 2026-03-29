from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))
from app.ml.simulator import simulate_race

router = APIRouter()

# 2026 F1 driver roster for simulations
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


class SimulationRequest(BaseModel):
    race_id: int = Field(..., description="ID of the race to simulate")
    weather: str = Field(..., description="Weather condition: 'dry', 'wet', or 'mixed'")
    grid_order: Optional[List[str]] = Field(None, description="Custom starting grid order (list of driver_ids)")
    excluded_drivers: Optional[List[str]] = Field(None, description="Driver IDs to exclude from simulation")

    class Config:
        json_schema_extra = {
            "example": {
                "race_id": 1,
                "weather": "wet",
                "grid_order": ["max_verstappen", "charles_leclerc", "lando_norris"],
                "excluded_drivers": ["lance_stroll"]
            }
        }


class DriverPrediction(BaseModel):
    driver_id: str
    driver_name: str
    team: str
    predicted_position: int
    confidence_score: float


class BaselinePrediction(BaseModel):
    driver_id: str
    predicted_position: int


class KeyFactor(BaseModel):
    factor: str
    impact: float
    criticality: str


class SimulationResponse(BaseModel):
    predictions: List[DriverPrediction]
    baseline_predictions: List[BaselinePrediction]
    key_factors: List[KeyFactor]

    class Config:
        json_schema_extra = {
            "example": {
                "predictions": [
                    {
                        "driver_id": "max_verstappen",
                        "driver_name": "Max Verstappen",
                        "team": "Red Bull Racing",
                        "predicted_position": 1,
                        "confidence_score": 0.92
                    }
                ],
                "baseline_predictions": [
                    {"driver_id": "max_verstappen", "predicted_position": 1}
                ],
                "key_factors": [
                    {"factor": "Grid Position", "impact": 0.85, "criticality": "Critical"}
                ]
            }
        }


@router.post("/simulate", response_model=SimulationResponse)
def run_simulation(request: SimulationRequest):
    """
    Run a race simulation with custom parameters.
    
    This endpoint powers the "what-if" scenario engine, allowing you to:
    - Change weather conditions (dry/wet/mixed)
    - Customize starting grid order
    - Exclude specific drivers
    
    Returns predictions, baseline comparison, and key factors affecting the race.
    """
    try:
        result = simulate_race(
            race_id=request.race_id,
            weather=request.weather,
            grid_order=request.grid_order,
            excluded_drivers=request.excluded_drivers,
            drivers=DRIVERS  # Use 2026 roster for future races
        )
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Simulation failed: {str(e)}"
        )


@router.get("/health")
def simulator_health():
    """Check if the simulator is ready."""
    try:
        from app.ml.model_loader import load_model
        model = load_model()
        return {
            "status": "ready",
            "model_loaded": model is not None
        }
    except Exception as e:
        return {
            "status": "error",
            "model_loaded": False,
            "error": str(e)
        }
