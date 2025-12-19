from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models.appointments import Appointments
from schemas.appointments import AppointmentsCreate, AppointmentUpdate

appointments_router=APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)

@appointments_router.post("/new_appointment")
def create_appointments(appointments:AppointmentsCreate ,db:Session=Depends(get_db)):
    new_appointments=Appointments(
       clients_id=appointments.clients_id,
        counsellors_id=appointments.counsellors_id,
        date=appointments.date,
        time=appointments.time,
        status=appointments.status
    )
    db.add(new_appointments)
    db.commit()
    db.refresh(new_appointments)
    return new_appointments
    
@appointments_router.get("/")
def get_all_appointments(db:Session=Depends(get_db)):
    already_book=db.query(Appointments).all()
    db.close()
    return already_book

@appointments_router.get("/{appointment_id}")
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointments).filter(Appointments.appointment_id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@appointments_router.put("/{appointment_id}")
def update_appointment(appointment_id: int, appointment: AppointmentUpdate, db: Session = Depends(get_db)):
    appointment = db.query(Appointments).filter(Appointments.appointment_id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.date = appointment.date
    appointment.time = appointment.time
    appointment.status = appointment.status
    db.commit()
    db.refresh(appointment)
    return appointment

@appointments_router.delete("/{appointments_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointments).filter(Appointments.appointment_id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    db.delete(appointment)
    db.commit()
    return {"message": "Appointment deleted successfully"}