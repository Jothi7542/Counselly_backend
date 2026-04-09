from fastapi import APIRouter , Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models.clients import Clients
from schemas.clients import ClientsCreate,ClientUpdate,Signup,Login, TokenResponse
from models.appointments import Appointments, AppointmentStatus
from models.counsellors import Counsellors
from utils.auth import hash_password, verify_password, create_access_token

clients_router=APIRouter(
    prefix="/clients",
    tags=["Clients"]
)

@clients_router.post("/signup", response_model=TokenResponse)
def signup(clients:Signup ,db:Session=Depends(get_db)):
    import traceback
    try:
        
        email = clients.email.strip().lower()
        password = clients.password.strip()

     
        existing_client = db.query(Clients).filter(Clients.email == email).first()
        if existing_client:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        new_client=Clients(
           name=clients.name,
           email=clients.email,
           password=hash_password(clients.password),  
           role="client",
           age=clients.age,
           gender=clients.gender,
           phone_number=clients.phone_number,
           language=clients.language,
           address=clients.address,
           profile_image=getattr(clients, 'profile_image', None)
        )
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        
        
        access_token = create_access_token(
            data={"sub": str(new_client.clients_id), "role": "client"}
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": new_client
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"SIGNUP ERROR: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@clients_router.post("/login", response_model=TokenResponse)
def login(data: Login, db: Session = Depends(get_db)):
    import traceback
    try:
        
        email = data.email.strip().lower()
        password = data.password.strip()

        client = db.query(Clients).filter(
            Clients.email == email
        ).first()

        if not client:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
       
        if not verify_password(password, client.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        
        access_token = create_access_token(
            data={"sub": str(client.clients_id), "role": "client"}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": client
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

    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])
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
        

@clients_router.get("/{client_id}/upcoming-sessions")
def upcoming_sessions(client_id: int, db: Session = Depends(get_db)):

    sessions = (
        db.query(
            Appointments.appointment_id,
            Appointments.counsellors_id,
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
            "counsellors_id": s.counsellors_id,
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
            Appointments.counsellors_id,
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
            "counsellors_id": s.counsellors_id,
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

