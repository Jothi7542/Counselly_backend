from pydantic import BaseModel
from datetime import date



class AvailabilityCreate(BaseModel):
    counsellors_id: int
    date: date
    day: str
    month: str
    time_slot: str
    session_period: str   
