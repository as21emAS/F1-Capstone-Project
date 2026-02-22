from fastapi import APIRouter, HTTPException
from functools import lru_cache
from datetime import datetime
import time

from app.schemas.races import NextRaceResponse, CircuitInfo

# Import your existing Jolpica client
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))
from api_clients.jolpica_f1_client import JolpicaF1Client

router = APIRouter()

# Simple cache: store (result, timestamp)
_next_race_cache = {"data": None, "timestamp": 0}
CACHE_TTL = 3600  # 1 hour

def get_cached_next_race():
    now = time.time()
    if _next_race_cache["data"] and (now - _next_race_cache["timestamp"]) < CACHE_TTL:
        return _next_race_cache["data"]
    return None

def set_cache(data):
    _next_race_cache["data"] = data
    _next_race_cache["timestamp"] = time.time()

@router.get("/next", response_model=NextRaceResponse)
def get_next_race():
    """Get the next upcoming F1 race"""
    
    # Check cache first
    cached = get_cached_next_race()
    if cached:
        return cached
   
    # Fetch from Jolpica
    client = JolpicaF1Client()
    race = client.get_next_race()
    
    if not race:
        raise HTTPException(status_code=404, detail="No upcoming race found")
    
    try:
        circuit = race.get("Circuit", {})
        location = circuit.get("Location", {})
        
        result = NextRaceResponse(
            race_name=race["raceName"],
            round_number=int(race["round"]),
            date=datetime.fromisoformat(race["date"]),
            time=race.get("time", "TBA").replace("Z", ""),
            circuit=CircuitInfo(
                name=circuit.get("circuitName", ""),
                location=location.get("locality", ""),
                country=location.get("country", "")
            ),
            season=int(race["season"])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error transforming race data: {str(e)}")
    
    set_cache(result)
    return result

