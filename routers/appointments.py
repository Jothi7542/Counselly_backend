from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db

from models.appointments import (
    Mode,
    SessionPeriod,
    Appointments,
    AppointmentStatus,
    CounsellorResponse
)

from models.availability import Availability

from schemas.appointments import (
    AppointmentsCreate,
    AppointmentUpdate,
    AppointmentResponseUpdate
)

appointments_router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


@appointments_router.post("/new_appointment")
def create_appointment(
    data: AppointmentsCreate,
    db: Session = Depends(get_db)
):
    availability = db.query(Availability).filter(
        Availability.availability_id == data.availability_id,
        Availability.is_booked == False
    ).first()

    if not availability:
        raise HTTPException(status_code=400, detail="Slot not available")

    appointment = Appointments(
        clients_id=data.clients_id,
        counsellors_id=data.counsellors_id,
        availability_id=availability.availability_id,

        date=availability.date,
        time=availability.time_slot,  

        mode=data.mode.lower(),        
        session_period=availability.session_period.lower(),  

        address=data.address,
        therapy_type=data.therapy_type,
        reason=data.reason,

        status=AppointmentStatus.booked.value,         
        counsellor_response=CounsellorResponse.pending.value
    )

    availability.is_booked = True

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment


@appointments_router.get("/")
def get_appointments(db: Session = Depends(get_db)):
    return db.query(Appointments).all()


@appointments_router.get("/{appointment_id}")
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointments).filter(
        Appointments.appointment_id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    return appointment


@appointments_router.put("/{appointment_id}")
def update_appointment(
    appointment_id: int,
    data: AppointmentUpdate,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointments).filter(
        Appointments.appointment_id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    if data.status is not None:
        appointment.status = data.status

    db.commit()
    db.refresh(appointment)

    return appointment

@appointments_router.put("/{appointment_id}/response")
def counsellor_response(
    appointment_id: int,
    data: AppointmentResponseUpdate,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointments).filter(
        Appointments.appointment_id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.counsellor_response = data.response

   
    if data.response == CounsellorResponse.rejected.value:
        availability = db.query(Availability).filter(
            Availability.availability_id == appointment.availability_id
        ).first()

        if availability:
            availability.is_booked = False

    db.commit()
    db.refresh(appointment)

    return appointment


@appointments_router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointments).filter(
        Appointments.appointment_id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    db.delete(appointment)
    db.commit()

    return {"message": "Appointment deleted successfully"}
