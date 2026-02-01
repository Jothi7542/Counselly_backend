from pydantic import BaseModel
from datetime import date , time
from typing import Optional
from models.appointments import Mode

from pydantic import BaseModel
from models.appointments import Mode

class AppointmentsCreate(BaseModel):
    clients_id: int
    counsellors_id: int
    availability_id: int
    mode: str
    address: str
    therapy_type: str
    reason: str


class AppointmentUpdate(BaseModel):
    status: Optional[str]

class AppointmentResponseUpdate(BaseModel):
    response: str  

