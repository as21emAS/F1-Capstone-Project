from pydantic import BaseModel
from typing import List


class DriverResponse(BaseModel):
    driver_id: str
    name: str
    team: str
    team_color: str
    country_flag: str
    number: int

    class Config:
        from_attributes = True


class DriversListResponse(BaseModel):
    drivers: List[DriverResponse]
    count: int
