from pydantic import BaseModel
from datetime import date

class AppointmentsCreate(BaseModel):
    clients_id:int
    counsellors_id:int
    date:date
    time:str
    status:str

class AppointmentUpdate(BaseModel):
    date: date
    time: str
    status: str

