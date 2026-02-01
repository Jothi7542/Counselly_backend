from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models.availability import Availability
from schemas.availability import AvailabilityCreate
from datetime import date
from fastapi import Query , HTTPException


availability_router = APIRouter(
    prefix="/availability",
    tags=["Availability"]
)

@availability_router.post("/create")
def create_availability(data: AvailabilityCreate, db: Session = Depends(get_db)):
    slot = Availability(
        counsellors_id=data.counsellors_id,
        date=data.date,
        day=data.day,
        month=data.month,
        time_slot=data.time_slot,
        session_period=data.session_period
    )
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot
@availability_router.get("/counsellor/{counsellor_id}")
def get_free_slots(
    counsellor_id: int,
    date: date = Query(...),
    db: Session = Depends(get_db)
):
    slots = db.query(Availability).filter(
        Availability.counsellors_id == counsellor_id,
        Availability.date == date,
        Availability.is_booked == False
    ).all()

    if not slots:
        raise HTTPException(
            status_code=404,
            detail="No available slots for this date"
        )

    response = {
        "morning": [],
        "afternoon": [],
        "evening": []
    }

    for slot in slots:
        period = slot.session_period.lower()
        if period in response:
             response[period].append({
                 "id": slot.availability_id,
                 "time": slot.time_slot
             })

    return response
