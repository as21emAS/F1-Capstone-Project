from fastapi import APIRouter
from app.schemas.standings import (
    DriverStandingsResponse, DriverStanding,
    TeamStandingsResponse, TeamStanding,
)

router = APIRouter()

SEASON = 2025

# 2025 driver standings — update as season progresses
DRIVER_STANDINGS = [
    {"position": 1,  "driver_id": "lando_norris",       "driver_name": "Lando Norris",        "team": "McLaren",        "points": 0.0, "wins": 0},
    {"position": 2,  "driver_id": "max_verstappen",     "driver_name": "Max Verstappen",      "team": "Red Bull Racing","points": 0.0, "wins": 0},
    {"position": 3,  "driver_id": "charles_leclerc",    "driver_name": "Charles Leclerc",     "team": "Ferrari",        "points": 0.0, "wins": 0},
    {"position": 4,  "driver_id": "oscar_piastri",      "driver_name": "Oscar Piastri",       "team": "McLaren",        "points": 0.0, "wins": 0},
    {"position": 5,  "driver_id": "carlos_sainz",       "driver_name": "Carlos Sainz",        "team": "Williams",       "points": 0.0, "wins": 0},
    {"position": 6,  "driver_id": "george_russell",     "driver_name": "George Russell",      "team": "Mercedes",       "points": 0.0, "wins": 0},
    {"position": 7,  "driver_id": "lewis_hamilton",     "driver_name": "Lewis Hamilton",      "team": "Ferrari",        "points": 0.0, "wins": 0},
    {"position": 8,  "driver_id": "fernando_alonso",    "driver_name": "Fernando Alonso",     "team": "Aston Martin",   "points": 0.0, "wins": 0},
    {"position": 9,  "driver_id": "pierre_gasly",       "driver_name": "Pierre Gasly",        "team": "Alpine",         "points": 0.0, "wins": 0},
    {"position": 10, "driver_id": "nico_hulkenberg",    "driver_name": "Nico Hulkenberg",     "team": "Sauber",         "points": 0.0, "wins": 0},
    {"position": 11, "driver_id": "yuki_tsunoda",       "driver_name": "Yuki Tsunoda",        "team": "RB",             "points": 0.0, "wins": 0},
    {"position": 12, "driver_id": "lance_stroll",       "driver_name": "Lance Stroll",        "team": "Aston Martin",   "points": 0.0, "wins": 0},
    {"position": 13, "driver_id": "oliver_bearman",     "driver_name": "Oliver Bearman",      "team": "Haas",           "points": 0.0, "wins": 0},
    {"position": 14, "driver_id": "esteban_ocon",       "driver_name": "Esteban Ocon",        "team": "Haas",           "points": 0.0, "wins": 0},
    {"position": 15, "driver_id": "alexander_albon",    "driver_name": "Alexander Albon",     "team": "Williams",       "points": 0.0, "wins": 0},
    {"position": 16, "driver_id": "liam_lawson",        "driver_name": "Liam Lawson",         "team": "Red Bull Racing","points": 0.0, "wins": 0},
    {"position": 17, "driver_id": "isack_hadjar",       "driver_name": "Isack Hadjar",        "team": "RB",             "points": 0.0, "wins": 0},
    {"position": 18, "driver_id": "andrea_antonelli",   "driver_name": "Andrea Kimi Antonelli","team": "Mercedes",      "points": 0.0, "wins": 0},
    {"position": 19, "driver_id": "jack_doohan",        "driver_name": "Jack Doohan",         "team": "Alpine",         "points": 0.0, "wins": 0},
    {"position": 20, "driver_id": "gabriel_bortoleto",  "driver_name": "Gabriel Bortoleto",   "team": "Sauber",         "points": 0.0, "wins": 0},
]

# 2025 constructor standings
TEAM_STANDINGS = [
    {"position": 1, "team": "McLaren",        "points": 0.0, "wins": 0},
    {"position": 2, "team": "Ferrari",        "points": 0.0, "wins": 0},
    {"position": 3, "team": "Red Bull Racing","points": 0.0, "wins": 0},
    {"position": 4, "team": "Mercedes",       "points": 0.0, "wins": 0},
    {"position": 5, "team": "Aston Martin",   "points": 0.0, "wins": 0},
    {"position": 6, "team": "Alpine",         "points": 0.0, "wins": 0},
    {"position": 7, "team": "Williams",       "points": 0.0, "wins": 0},
    {"position": 8, "team": "RB",             "points": 0.0, "wins": 0},
    {"position": 9, "team": "Haas",           "points": 0.0, "wins": 0},
    {"position": 10,"team": "Sauber",         "points": 0.0, "wins": 0},
]


@router.get("/drivers/current", response_model=DriverStandingsResponse)
def get_driver_standings():
    """Get 2025 season driver championship standings."""
    return DriverStandingsResponse(
        season=SEASON,
        standings=[DriverStanding(**d) for d in DRIVER_STANDINGS],
    )


@router.get("/teams/current", response_model=TeamStandingsResponse)
def get_team_standings():
    """Get 2025 season constructor championship standings."""
    return TeamStandingsResponse(
        season=SEASON,
        standings=[TeamStanding(**t) for t in TEAM_STANDINGS],
    )