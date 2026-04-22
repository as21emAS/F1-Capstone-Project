from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CircuitInfo(BaseModel):
    name: str
    location: str
    country: str
    timezone: Optional[str] = None

class NextRaceResponse(BaseModel):
    race_name: str
    round_number: int
    date: datetime
    time: str
    circuit: CircuitInfo
    season: int

