from pydantic import BaseModel
from typing import List


class DriverStanding(BaseModel):
    position: int
    driver_id: str
    driver_name: str
    team: str
    points: float
    wins: int


class TeamStanding(BaseModel):
    position: int
    team: str
    points: float
    wins: int


class DriverStandingsResponse(BaseModel):
    season: int
    standings: List[DriverStanding]


class TeamStandingsResponse(BaseModel):
    season: int
    standings: List[TeamStanding]