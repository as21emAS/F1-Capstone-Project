from fastapi import APIRouter, HTTPException
from app.schemas.standings import (
    DriverStandingsResponse, DriverStanding,
    TeamStandingsResponse, TeamStanding,
)
from app.core.config import settings
import time
import os
import psycopg2
import psycopg2.extras

from app.external.jolpica import JolpicaF1Client
#import fastf1.plotting

TEAM_COLORS = {
    "Mercedes": "#27F4D2",
    "Ferrari": "#E8002D",
    "McLaren": "#FF8000",
    "Red Bull": "#3671C6",
    "Aston Martin": "#229971",
    "Alpine F1 Team": "#FF87CC",
    "Williams": "#64C4FF",
    "RB F1 Team": "#6692FF",
    "Haas F1 Team": "#B6BABD",
    "Audi": "#999966",
    "Cadillac F1 Team": "#FFFFFF",
}

def _get_team_color(team_name: str) -> str:
    return TEAM_COLORS.get(team_name, "#000000")

router = APIRouter()

SEASON = settings.CURRENT_SEASON

_cache = {
    "drivers": {"data": None, "timestamp": 0},
    "teams":   {"data": None, "timestamp": 0},
}
CACHE_TTL = 300  # 5 minutes


def _is_cached(key: str) -> bool:
    return _cache[key]["data"] is not None and (time.time() - _cache[key]["timestamp"]) < CACHE_TTL


def _set_cache(key: str, data):
    _cache[key]["data"] = data
    _cache[key]["timestamp"] = time.time()


def _get_db():
    return psycopg2.connect(os.getenv("DATABASE_URL"))


@router.get("/drivers/current", response_model=DriverStandingsResponse)
def get_driver_standings():
    if _is_cached("drivers"):
        return _cache["drivers"]["data"]

    # Try DB first
    try:
        conn = _get_db()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("""
            SELECT
                ds.position,
                ds.driver_id,
                d.driver_full_name AS driver_name,
                COALESCE(t.team_name, '') AS team,
                ds.points,
                ds.wins
            FROM driver_standings ds
            JOIN drivers d ON ds.driver_id = d.driver_id
            LEFT JOIN (
                SELECT DISTINCT ON (rr.driver_id)
                    rr.driver_id,
                    t2.team_name
                FROM race_results rr
                JOIN teams t2 ON rr.team_id = t2.team_id
                JOIN races r ON rr.race_id = r.race_id
                WHERE r.year = %s
                ORDER BY rr.driver_id, r.date DESC
            ) t ON t.driver_id = ds.driver_id
            WHERE ds.year = %s
            ORDER BY ds.position ASC
        """, (SEASON, SEASON))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        rows = []

    if rows:
        standings = [
            DriverStanding(
                position=row["position"],
                #driver_id=row["driver_id"],
                driver_name=row["driver_name"],
                team=row["team"],
                points=float(row["points"]),
                #wins=row["wins"],
                win_chance=0.0,
            )
            for row in rows
        ]
        result = DriverStandingsResponse(season=SEASON, standings=standings)
        _set_cache("drivers", result)
        return result

    # Fallback to Jolpica
    client = JolpicaF1Client()
    raw = client.get_driver_standings(SEASON)

    if not raw:
        raise HTTPException(status_code=503, detail="Could not fetch driver standings")

    standings = []
    for entry in raw:
        driver = entry.get("Driver", {})
        constructors = entry.get("Constructors", [{}])
        team_name = constructors[0].get("name", "") if constructors else ""
        given = driver.get("givenName", "")
        family = driver.get("familyName", "")

        standings.append(DriverStanding(
            position=int(entry.get("position", 0)),
            #driver_id=driver.get("driverId", ""),
            driver_name=f"{given} {family}".strip(),
            team=team_name,
            points=float(entry.get("points", 0)),
            #wins=int(entry.get("wins", 0)),
            win_chance=0.0,
        ))

    result = DriverStandingsResponse(season=SEASON, standings=standings)
    _set_cache("drivers", result)
    return result

@router.get("/teams/current", response_model=TeamStandingsResponse)
def get_team_standings():
    if _is_cached("teams"):
        return _cache["teams"]["data"]

    # Try DB first
    try:
        conn = _get_db()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("""
            SELECT
                ts.position,
                t.team_name,
                ts.points
            FROM team_standings ts
            JOIN teams t ON ts.team_id = t.team_id
            WHERE ts.year = %s
            ORDER BY ts.position ASC
        """, (SEASON,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        rows = []

    if rows:
        standings = [
            TeamStanding(
                position=row["position"],
                team_name=row["team_name"],
                points=float(row["points"]),
                color=_get_team_color(row["team_name"]),  # ← FastF1 color
                win_chance=0.0,
            )
            for row in rows
        ]
        result = TeamStandingsResponse(season=SEASON, standings=standings)
        _set_cache("teams", result)
        return result

    # Fallback to Jolpica
    client = JolpicaF1Client()
    raw = client.get_constructor_standings(SEASON)

    if not raw:
        raise HTTPException(status_code=503, detail="Could not fetch constructor standings from Jolpica API")

    standings = []
    for entry in raw:
        constructor = entry.get("Constructor", {})
        standings.append(TeamStanding(
            position=int(entry.get("position", 0)),
            team_name=constructor.get("name", ""),
            points=float(entry.get("points", 0)),
            color=_get_team_color(constructor.get("name", "")),  # team color
            win_chance=0.0,
        ))

    result = TeamStandingsResponse(season=SEASON, standings=standings)
    _set_cache("teams", result)
    return result