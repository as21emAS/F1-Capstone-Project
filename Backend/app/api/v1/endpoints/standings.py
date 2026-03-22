from fastapi import APIRouter, HTTPException
from app.schemas.standings import (
    DriverStandingsResponse, DriverStanding,
    TeamStandingsResponse, TeamStanding,
)
from app.core.config import settings
import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from api_clients.jolpica_f1_client import JolpicaF1Client

router = APIRouter()

SEASON = settings.CURRENT_SEASON

# Simple in-memory cache to avoid hammering the API
_cache = {
    "drivers": {"data": None, "timestamp": 0},
    "teams":   {"data": None, "timestamp": 0},
}
CACHE_TTL = 3600  # 1 hour


def _is_cached(key: str) -> bool:
    return _cache[key]["data"] is not None and (time.time() - _cache[key]["timestamp"]) < CACHE_TTL


def _set_cache(key: str, data):
    _cache[key]["data"] = data
    _cache[key]["timestamp"] = time.time()


@router.get("/drivers/current", response_model=DriverStandingsResponse)
def get_driver_standings():
    """Get current season driver championship standings (live from Jolpica)."""
    if _is_cached("drivers"):
        return _cache["drivers"]["data"]

    client = JolpicaF1Client()
    raw = client.get_driver_standings(SEASON)

    if not raw:
        raise HTTPException(status_code=503, detail="Could not fetch driver standings from Jolpica API")

    standings = []
    for entry in raw:
        driver = entry.get("Driver", {})
        constructors = entry.get("Constructors", [{}])
        team_name = constructors[0].get("name", "") if constructors else ""

        given = driver.get("givenName", "")
        family = driver.get("familyName", "")

        standings.append(DriverStanding(
            position=int(entry.get("position", 0)),
            driver_id=driver.get("driverId", ""),
            driver_name=f"{given} {family}".strip(),
            team=team_name,
            points=float(entry.get("points", 0)),
            wins=int(entry.get("wins", 0)),
        ))

    result = DriverStandingsResponse(season=SEASON, standings=standings)
    _set_cache("drivers", result)
    return result


@router.get("/teams/current", response_model=TeamStandingsResponse)
def get_team_standings():
    """Get current season constructor championship standings (live from Jolpica)."""
    if _is_cached("teams"):
        return _cache["teams"]["data"]

    client = JolpicaF1Client()
    raw = client.get_constructor_standings(SEASON)

    if not raw:
        raise HTTPException(status_code=503, detail="Could not fetch constructor standings from Jolpica API")

    standings = []
    for entry in raw:
        constructor = entry.get("Constructor", {})
        standings.append(TeamStanding(
            position=int(entry.get("position", 0)),
            team=constructor.get("name", ""),
            points=float(entry.get("points", 0)),
            wins=int(entry.get("wins", 0)),
        ))

    result = TeamStandingsResponse(season=SEASON, standings=standings)
    _set_cache("teams", result)
    return result