from fastapi import APIRouter , Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models.clients import Clients
from schemas.clients import ClientsCreate,ClientUpdate,Signup,Login
from utils.auth import hash_password, verify_password, create_access_token

clients_router=APIRouter(
    prefix="/clients",
    tags=["Clients"]
)

@clients_router.post("/signup")
def signup(clients:Signup ,db:Session=Depends(get_db)):
    import traceback
    try:
        # Check if email already exists
        existing_client = db.query(Clients).filter(Clients.email == clients.email).first()
        if existing_client:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        signup=Clients(
           name=clients.name,
           email=clients.email,
           password=hash_password(clients.password),  # Hash the password
           age=clients.age,
           gender=clients.gender,
           phone_number=clients.phone_number,
           language=clients.language,
           address=clients.address,
           profile_image=clients.profile_image
        )
        db.add(signup)
        db.commit()
        db.refresh(signup)
        
        # Create access token
        access_token = create_access_token(
            data={"sub": str(signup.clients_id), "role": "client"}
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "clients_id": signup.clients_id,
                "name": signup.name,
                "email": signup.email,
                "profile_image": signup.profile_image,
                "role": "client"
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"SIGNUP ERROR: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@clients_router.post("/login")
def login(data: Login, db: Session = Depends(get_db)):
    import traceback
    try:
        client = db.query(Clients).filter(
            Clients.email == data.email
        ).first()

        if not client:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Verify password
        if not verify_password(data.password, client.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create access token
        access_token = create_access_token(
            data={"sub": str(client.clients_id), "role": "client"}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "clients_id": client.clients_id,
                "name": client.name,
                "email": client.email,
                "age": client.age,
                "gender": client.gender,
                "phone_number": client.phone_number,
                "language": client.language,
                "address": client.address,
                "profile_image": client.profile_image,
                "role": "client"
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"LOGIN ERROR: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@clients_router.post("/create")
def add_clients(clients: ClientsCreate, db: Session = Depends(get_db)):
    new_clients = Clients(
        clients_id=clients.clients_id,
        name=clients.name,
        email=clients.email,
        password=hash_password(clients.password),
        age=clients.age,
        gender=clients.gender,
        phone_number=clients.phone_number,
        language=clients.language,
        status=clients.status,
        address=clients.address,
        created_at=clients.created_at    
    )
    db.add(new_clients)
    db.commit()
    db.refresh(new_clients)
    return new_clients


@clients_router.get("/")
def all_clients(db:Session=Depends(get_db)):
    already_clients=db.query(Clients).all()
    db.close()
    return already_clients

@clients_router.get("/{clients_id}")
def clients_id(clients_id:int , db:Session=Depends(get_db)):
    already_clients=db.query(Clients).filter(Clients.clients_id==clients_id).first()
    db.close()
    return already_clients

from fastapi import HTTPException

@clients_router.put("/update/{clients_id}")
def update_clients(
    clients_id: int,
    data: ClientUpdate,
    db: Session = Depends(get_db)
):
    client = db.query(Clients).filter(
        Clients.clients_id == clients_id
    ).first()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    update_data = data.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(client, field, value)

    db.commit()
    db.refresh(client)
    return client


@clients_router.delete("/deleteClients/{clients_id}")
def delete_clients(clients_id:int , db:Session=Depends(get_db)):
    delete_clients=db.query(Clients).filter(Clients.clients_id==clients_id).first()
    if delete_clients:
        db.delete(delete_clients)
        db.commit()
        return {"message": "Clients deleted successfully"}
    return {"message": "Clients not found"}
        

from models.appointments import Appointments, AppointmentStatus
from models.counsellors import Counsellors

@clients_router.get("/{client_id}/upcoming-sessions")
def upcoming_sessions(client_id: int, db: Session = Depends(get_db)):

    sessions = (
        db.query(
            Appointments.appointment_id,
            Appointments.date,
            Appointments.time,
            Appointments.mode,
            Appointments.session_period,
            Appointments.therapy_type,
            Appointments.status,
            Counsellors.name.label("counsellor_name"),
            Counsellors.profile_image.label("counsellor_photo")
        )
        .join(Counsellors, Counsellors.counsellors_id == Appointments.counsellors_id)
        .filter(
            Appointments.clients_id == client_id,
            Appointments.status.in_([AppointmentStatus.booked.value, AppointmentStatus.pending.value])

        )
        .all()
    )

    return [
        {
            "appointment_id": s.appointment_id,
            "date": s.date,
            "time": s.time,
            "mode": s.mode,
            "session_period": s.session_period,
            "therapy_type": s.therapy_type,
            "status": s.status,
            "counsellor_name": s.counsellor_name,
            "counsellor_photo": s.counsellor_photo
        }
        for s in sessions
    ]

@clients_router.get("/{client_id}/completed-sessions")
def completed_sessions(client_id: int, db: Session = Depends(get_db)):

    sessions = (
        db.query(
            Appointments.appointment_id,
            Appointments.date,
            Appointments.time,
            Appointments.mode,
            Appointments.session_period,
            Appointments.therapy_type,
            Counsellors.name.label("counsellor_name"),
            Counsellors.profile_image.label("counsellor_photo")
        )
        .join(Counsellors, Counsellors.counsellors_id == Appointments.counsellors_id)
        .filter(
            Appointments.clients_id == client_id,
            Appointments.status == AppointmentStatus.completed.value

        )
        .all()
    )

    return [
        {
            "appointment_id": s.appointment_id,
            "date": s.date,
            "time": s.time,
            "mode": s.mode,
            "session_period": s.session_period,
            "therapy_type": s.therapy_type,
            "counsellor_name": s.counsellor_name,
            "counsellor_photo": s.counsellor_photo
        }
        for s in sessions
    ]

