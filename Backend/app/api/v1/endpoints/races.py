from fastapi import APIRouter, HTTPException
from functools import lru_cache
from datetime import datetime, date
import time

from app.schemas.races import NextRaceResponse, CircuitInfo
from pydantic import BaseModel

from app.external.jolpica import JolpicaF1Client

router = APIRouter()

# ─── Cache ──────────────────────────────────────────────────────────────────
_next_race_cache:     dict = {"data": None, "timestamp": 0}
_upcoming_races_cache: dict = {"data": None, "timestamp": 0}
CACHE_TTL = 3600  # 1 hour


def _is_fresh(cache: dict) -> bool:
    return cache["data"] is not None and (time.time() - cache["timestamp"]) < CACHE_TTL


def _set(cache: dict, data) -> None:
    cache["data"] = data
    cache["timestamp"] = time.time()


class UpcomingRace(BaseModel):
    race_id: int          # equals round_number — used as the prediction request ID
    round_number: int
    race_name: str
    circuit_name: str
    country: str
    date: str             # ISO date string e.g. "2025-03-23"
    season: int

# ─── /next ──────────────────────────────────────────────────────────────────

@router.get("/next", response_model=NextRaceResponse)
def get_next_race():
    """Get the next upcoming F1 race."""
    if _is_fresh(_next_race_cache):
        return _next_race_cache["data"]

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
                country=location.get("country", ""),
            ),
            season=int(race["season"]),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error transforming race data: {str(e)}")

    _set(_next_race_cache, result)
    return result


# ─── /upcoming ──────────────────────────────────────────────────────────────

@router.get("/upcoming", response_model=list[UpcomingRace])
def get_upcoming_races():
    """
    Return all remaining 2025 races (today onwards), sorted by round.
    Used to populate the race dropdown in the Simulator.
    """
    if _is_fresh(_upcoming_races_cache):
        return _upcoming_races_cache["data"]

    client = JolpicaF1Client()
    all_races = client.get_race_schedule(2026)

    if not all_races:
        raise HTTPException(status_code=503, detail="Could not fetch 2025 race schedule")

    today = date.today()
    upcoming = []

    for race in all_races:
        try:
            race_date = date.fromisoformat(race["date"])
            if race_date >= today:
                circuit = race.get("Circuit", {})
                location_data = circuit.get("Location", {})
                upcoming.append(
                    UpcomingRace(
                        race_id=int(race["round"]),   # use round as ID for predictions
                        round_number=int(race["round"]),
                        race_name=race["raceName"],
                        circuit_name=circuit.get("circuitName", ""),
                        country=location_data.get("country", ""),
                        date=race["date"],
                        season=int(race["season"]),
                    )
                )
        except (KeyError, ValueError):
            continue

    upcoming.sort(key=lambda r: r.round_number)
    _set(_upcoming_races_cache, upcoming)
    return upcoming