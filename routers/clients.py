from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from models.clients import Clients
from schemas.clients import ClientsCreate,ClientUpdate,Signup,Login, TokenResponse
from auth_utils import get_password_hash, verify_password, create_access_token

clients_router=APIRouter(
    prefix="/clients",
    tags=["Clients"]
)

@clients_router.post("/signup", response_model=TokenResponse)
def signup(clients:Signup ,db:Session=Depends(get_db)):
    new_client=Clients(
       name=clients.name,
       email=clients.email,
       password=get_password_hash(clients.password),
       role="client",
       age=clients.age,
       gender=clients.gender,
       phone_number=clients.phone_number,
       language=clients.language,
       address=clients.address
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    
    access_token = create_access_token(data={"sub": new_client.email, "role": "client"})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": new_client
    }

from fastapi import HTTPException

@clients_router.post("/login", response_model=TokenResponse)
def login(data: Login, db: Session = Depends(get_db)):
    client = db.query(Clients).filter(Clients.email == data.email).first()

    if not client or not verify_password(data.password, client.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": client.email, "role": "client"})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": client
    }


@clients_router.post("/create")
def add_clients(clients: ClientsCreate, db: Session = Depends(get_db)):
    new_clients = Clients(
        clients_id=clients.clients_id,
        name=clients.name,
        email=clients.email,
        password=get_password_hash(clients.password),
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

    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])

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
            Counsellors.name.label("counsellor_name"),
            Counsellors.profile_image.label("counsellor_photo")
        )
        .join(Counsellors, Counsellors.counsellors_id == Appointments.counsellors_id)
        .filter(
            Appointments.clients_id == client_id,
            Appointments.status == AppointmentStatus.booked.value

        )
        .all()
    )

    return sessions

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

    return sessions

