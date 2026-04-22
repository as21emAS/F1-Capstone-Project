from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.drivers import DriverResponse, DriversListResponse
from database.database import get_db
from app.models.models import Driver, Team

router = APIRouter()

# 2026 F1 Driver Grid - Hardcoded fallback
DRIVERS_2026 = [
    {"driver_id": "hamilton", "name": "Lewis Hamilton", "team": "Mercedes", "team_color": "#27F4D2", "country_flag": "🇬🇧", "number": 44},
    {"driver_id": "russell", "name": "George Russell", "team": "Mercedes", "team_color": "#27F4D2", "country_flag": "🇬🇧", "number": 63},
    {"driver_id": "leclerc", "name": "Charles Leclerc", "team": "Ferrari", "team_color": "#E8002D", "country_flag": "🇲🇨", "number": 16},
    {"driver_id": "sainz", "name": "Carlos Sainz", "team": "Ferrari", "team_color": "#E8002D", "country_flag": "🇪🇸", "number": 55},
    {"driver_id": "norris", "name": "Lando Norris", "team": "McLaren", "team_color": "#FF8000", "country_flag": "🇬🇧", "number": 4},
    {"driver_id": "piastri", "name": "Oscar Piastri", "team": "McLaren", "team_color": "#FF8000", "country_flag": "🇦🇺", "number": 81},
    {"driver_id": "verstappen", "name": "Max Verstappen", "team": "Red Bull Racing", "team_color": "#3671C6", "country_flag": "🇳🇱", "number": 1},
    {"driver_id": "perez", "name": "Sergio Pérez", "team": "Red Bull Racing", "team_color": "#3671C6", "country_flag": "🇲🇽", "number": 11},
    {"driver_id": "alonso", "name": "Fernando Alonso", "team": "Aston Martin", "team_color": "#229971", "country_flag": "🇪🇸", "number": 14},
    {"driver_id": "stroll", "name": "Lance Stroll", "team": "Aston Martin", "team_color": "#229971", "country_flag": "🇨🇦", "number": 18},
    {"driver_id": "gasly", "name": "Pierre Gasly", "team": "Alpine", "team_color": "#FF87BC", "country_flag": "🇫🇷", "number": 10},
    {"driver_id": "doohan", "name": "Jack Doohan", "team": "Alpine", "team_color": "#FF87BC", "country_flag": "🇦🇺", "number": 7},
    {"driver_id": "albon", "name": "Alex Albon", "team": "Williams", "team_color": "#64C4FF", "country_flag": "🇹🇭", "number": 23},
    {"driver_id": "colapinto", "name": "Franco Colapinto", "team": "Williams", "team_color": "#64C4FF", "country_flag": "🇦🇷", "number": 43},
    {"driver_id": "tsunoda", "name": "Yuki Tsunoda", "team": "Racing Bulls", "team_color": "#6692FF", "country_flag": "🇯🇵", "number": 22},
    {"driver_id": "hadjar", "name": "Isack Hadjar", "team": "Racing Bulls", "team_color": "#6692FF", "country_flag": "🇫🇷", "number": 21},
    {"driver_id": "bearman", "name": "Oliver Bearman", "team": "Haas", "team_color": "#B6BABD", "country_flag": "🇬🇧", "number": 87},
    {"driver_id": "ocon", "name": "Esteban Ocon", "team": "Haas", "team_color": "#B6BABD", "country_flag": "🇫🇷", "number": 31},
    {"driver_id": "hulkenberg", "name": "Nico Hülkenberg", "team": "Audi", "team_color": "#FF1E00", "country_flag": "🇩🇪", "number": 27},
    {"driver_id": "bortoleto", "name": "Gabriel Bortoleto", "team": "Audi", "team_color": "#FF1E00", "country_flag": "🇧🇷", "number": 5},
    {"driver_id": "drugovich", "name": "Felipe Drugovich", "team": "Cadillac", "team_color": "#1E3A8A", "country_flag": "🇧🇷", "number": 50},
    {"driver_id": "maini", "name": "Kush Maini", "team": "Cadillac", "team_color": "#1E3A8A", "country_flag": "🇮🇳", "number": 51},
]

# Team color mapping for DB-based queries
TEAM_COLORS = {
    "mercedes": "#27F4D2",
    "ferrari": "#E8002D",
    "mclaren": "#FF8000",
    "red_bull": "#3671C6",
    "aston_martin": "#229971",
    "alpine": "#FF87BC",
    "williams": "#64C4FF",
    "rb": "#6692FF",  # Racing Bulls
    "haas": "#B6BABD",
    "sauber": "#FF1E00",  # Audi/Sauber
    "kick_sauber": "#FF1E00",
    "audi": "#FF1E00",
    "cadillac": "#1E3A8A",
}

# Country flags mapping (ISO alpha-3 to emoji)
COUNTRY_FLAGS = {
    "British": "🇬🇧",
    "Monegasque": "🇲🇨",
    "Spanish": "🇪🇸",
    "Australian": "🇦🇺",
    "Dutch": "🇳🇱",
    "Mexican": "🇲🇽",
    "Canadian": "🇨🇦",
    "French": "🇫🇷",
    "Thai": "🇹🇭",
    "Argentine": "🇦🇷",
    "Japanese": "🇯🇵",
    "German": "🇩🇪",
    "Brazilian": "🇧🇷",
    "Indian": "🇮🇳",
}


@router.get("/", response_model=DriversListResponse)
async def get_drivers(db: Session = Depends(get_db)):
    """
    Get all 2026 F1 drivers.
    
    Returns list with driver_id, name, team, team_color, country_flag, and number.
    
    NOTE: Returns hardcoded 2026 grid since DB contains historical drivers
    without season filtering. In future, could  query DB with season=2026 filter.
    """

    drivers_list = [DriverResponse(**driver) for driver in DRIVERS_2026]
    return DriversListResponse(drivers=drivers_list, count=len(drivers_list))
