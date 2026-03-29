from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import date as DateType


# ── Pagination ────────────────────────────────────────────────────────────────

class PaginatedResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: List[Any]


# ── Circuits ──────────────────────────────────────────────────────────────────

class CircuitSummary(BaseModel):
    circuit_id: str
    circuit_name: str
    location: Optional[str] = None
    country: Optional[str] = None


class CircuitDetail(BaseModel):
    circuit_id: str
    circuit_name: str
    location: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


# ── Races ─────────────────────────────────────────────────────────────────────

class RaceSummary(BaseModel):
    race_id: int
    season: int
    round: int
    race_name: str
    circuit_id: str
    circuit_name: Optional[str] = None
    country: Optional[str] = None
    date: Optional[DateType] = None


class RaceDetail(BaseModel):
    race_id: int
    season: int
    round: int
    race_name: str
    circuit_id: str
    circuit_name: Optional[str] = None
    country: Optional[str] = None
    date: Optional[DateType] = None


# ── Race Results ──────────────────────────────────────────────────────────────

class RaceResult(BaseModel):
    position: Optional[int] = None
    position_text: Optional[str] = None
    driver_id: str
    driver_name: str
    team: str
    grid: Optional[int] = None
    points: Optional[float] = None
    status: Optional[str] = None
    laps_completed: Optional[int] = None
    dnf: Optional[bool] = None


class RaceResultsResponse(BaseModel):
    race_id: int
    race_name: str
    season: int
    round: int
    results: List[RaceResult]