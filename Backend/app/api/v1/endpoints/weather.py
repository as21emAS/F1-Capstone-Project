from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import time

from app.core.config import settings
from database.crud import get_db_connection
from database.connection_pool import return_connection
from api_clients.openweather_client import OpenWeatherClient

router = APIRouter()

# ─── Cache ──────────────────────────────────────────────────────────────────
_weather_cache: dict = {}
CACHE_TTL = 3600  # 1 hour


def _get_cached(key: str) -> Optional[dict]:
    if key in _weather_cache:
        data, timestamp = _weather_cache[key]
        if time.time() - timestamp < CACHE_TTL:
            return data
    return None


def _set_cache(key: str, data: dict):
    _weather_cache[key] = (data, time.time())


# ─── Schemas ────────────────────────────────────────────────────────────────

class WeatherResponse(BaseModel):
    temperature: float
    humidity: int
    conditions: str
    wind_speed: float
    rainfall: float
    forecast_time: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "temperature": 24.5,
                "humidity": 65,
                "conditions": "partly cloudy",
                "wind_speed": 3.2,
                "rainfall": 0.0,
                "forecast_time": "2026-04-12T14:00:00"
            }
        }


class CircuitWeatherResponse(BaseModel):
    circuit_id: str
    circuit_name: str
    location: Optional[str] = None
    country: Optional[str] = None
    weather: WeatherResponse
    summary: str  # human-readable summary


class RaceWeatherResponse(BaseModel):
    race_id: int
    race_name: str
    circuit_name: str
    date: str
    weather: WeatherResponse
    summary: str


# ─── Helper Functions ───────────────────────────────────────────────────────

def fetch_circuit_by_id(circuit_id: str) -> Optional[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM circuits WHERE circuit_id = %s", (circuit_id,))
    row = cursor.fetchone()
    cursor.close()
    return_connection(conn)
    return dict(row) if row else None


def fetch_race_by_id(race_id: int) -> Optional[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, c.circuit_name, c.latitude, c.longitude
        FROM races r
        JOIN circuits c ON r.circuit_id = c.circuit_id
        WHERE r.race_id = %s
    """, (race_id,))
    row = cursor.fetchone()
    cursor.close()
    return_connection(conn)
    return dict(row) if row else None


def get_weather_client() -> OpenWeatherClient:
    if not settings.OPENWEATHER_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="Weather service not configured. OPENWEATHER_API_KEY missing."
        )
    
    return OpenWeatherClient(api_key=settings.OPENWEATHER_API_KEY, cache_hours=1)


def format_weather_summary(weather: dict) -> str:
    temp = weather['temperature']
    condition = weather['conditions']
    rain = weather['rainfall']
    
    if rain > 0:
        return f"{condition.title()}, {temp}°C (Wet conditions - {rain}mm rain)"
    else:
        return f"{condition.title()}, {temp}°C"


# ─── Endpoints ──────────────────────────────────────────────────────────────

@router.get("/circuit/{circuit_id}", response_model=CircuitWeatherResponse)
def get_circuit_weather(circuit_id: str):
    """
    Get current weather conditions at a circuit location.
    
    Uses circuit coordinates to fetch real-time weather from OpenWeather API.
    Results are cached for 1 hour.
    """
    # check cache first
    cache_key = f"circuit_{circuit_id}"
    cached = _get_cached(cache_key)
    if cached:
        return cached
    
    # get circuit from database
    circuit = fetch_circuit_by_id(circuit_id)
    
    if not circuit:
        raise HTTPException(status_code=404, detail=f"Circuit '{circuit_id}' not found")
    
    # verify coordinates exist
    if not circuit.get('latitude') or not circuit.get('longitude'):
        raise HTTPException(
            status_code=400,
            detail=f"Circuit '{circuit_id}' has no coordinates available"
        )
    
    # get weather client
    client = get_weather_client()
    
    # fetch weather
    weather_data = client.get_current_weather(
        lat=float(circuit['latitude']),
        lon=float(circuit['longitude'])
    )
    
    if not weather_data:
        raise HTTPException(
            status_code=503,
            detail="Weather service temporarily unavailable"
        )
    
    # build response
    response = CircuitWeatherResponse(
        circuit_id=circuit['circuit_id'],
        circuit_name=circuit['circuit_name'],
        location=circuit.get('location'),
        country=circuit.get('country'),
        weather=WeatherResponse(**weather_data),
        summary=format_weather_summary(weather_data)
    )
    
    # cache the response
    _set_cache(cache_key, response)
    
    return response


@router.get("/race/{race_id}", response_model=RaceWeatherResponse)
def get_race_weather(race_id: int):
    """
    Get weather forecast for an upcoming race.
    
    - If race is today or in the past: returns current weather
    - If race is within 5 days: returns forecast for race time
    - If race is beyond 5 days: returns error (free tier limitation)
    
    Results are cached for 1 hour.
    """
    # check cache first
    cache_key = f"race_{race_id}"
    cached = _get_cached(cache_key)
    if cached:
        return cached
    
    # get race from database
    race = fetch_race_by_id(race_id)
    
    if not race:
        raise HTTPException(status_code=404, detail=f"Race with ID {race_id} not found")
    
    # verify coordinates exist
    if not race.get('latitude') or not race.get('longitude'):
        raise HTTPException(
            status_code=400,
            detail=f"Circuit coordinates not available for race {race_id}"
        )
    
    # get weather client
    client = get_weather_client()
    
    # convert race date to datetime
    race_date = datetime.combine(race['date'], datetime.min.time().replace(hour=14))  # Assume 2pm race time
    
    # fetch weather for race date
    weather_data = client.get_race_weather(
        lat=float(race['latitude']),
        lon=float(race['longitude']),
        race_date=race_date
    )
    
    if not weather_data:
        raise HTTPException(
            status_code=503,
            detail="Weather forecast unavailable (race may be beyond 5-day forecast range)"
        )
    
    # build response
    response = RaceWeatherResponse(
        race_id=race['race_id'],
        race_name=race['race_name'],
        circuit_name=race['circuit_name'],
        date=str(race['date']),
        weather=WeatherResponse(**weather_data),
        summary=format_weather_summary(weather_data)
    )
    
    # cache the response
    _set_cache(cache_key, response)
    
    return response


@router.get("/summary/{circuit_id}")
def get_weather_summary(circuit_id: str):
    """
    Get a simple weather summary string for a circuit.
    """
    # check cache first
    cache_key = f"summary_{circuit_id}"
    cached = _get_cached(cache_key)
    if cached:
        return cached
    
    # get circuit from database
    circuit = fetch_circuit_by_id(circuit_id)
    
    if not circuit:
        raise HTTPException(status_code=404, detail=f"Circuit '{circuit_id}' not found")
    
    if not circuit.get('latitude') or not circuit.get('longitude'):
        raise HTTPException(
            status_code=400,
            detail=f"Circuit '{circuit_id}' has no coordinates"
        )
    
    # get weather client and fetch summary
    client = get_weather_client()
    summary = client.get_weather_summary(
        lat=float(circuit['latitude']),
        lon=float(circuit['longitude'])
    )
    
    if not summary:
        raise HTTPException(
            status_code=503,
            detail="Weather service temporarily unavailable"
        )
    
    response = {
        "circuit_id": circuit_id,
        "summary": summary
    }
    
    # cache the response
    _set_cache(cache_key, response)
    
    return response
