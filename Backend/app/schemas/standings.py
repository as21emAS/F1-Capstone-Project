from pydantic import BaseModel
from typing import List


class DriverStanding(BaseModel):
    position: int
    #driver_id: str
    driver_name: str
    team: str
    points: float
    #wins: int
    win_chance: float = 0.0  

class TeamStanding(BaseModel):
    position: int
    team_name: str
    points: float
    color: str = "#000000"
    win_chance: float = 0.0

class DriverStandingsResponse(BaseModel):
    season: int
    standings: List[DriverStanding]


class TeamStandingsResponse(BaseModel):
    season: int
    standings: List[TeamStanding]