from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from models.clients import Clients
from schemas.clients import ClientsCreate,ClientUpdate,Signup,Login

clients_router=APIRouter(
    prefix="/clients",
    tags=["Clients"]
)

@clients_router.post("/signup")
def signup(clients:Signup ,db:Session=Depends(get_db)):
    signup=Clients(
       name=clients.name,
       email=clients.email,
       password=clients.password,
       role=clients.role,
       age=clients.age,
       gender=clients.gender,
       phone_number=clients.phone_number,
       language=clients.language,
       address=clients.address
    )
    db.add(signup)
    db.commit()
    db.refresh(signup)
    return signup

@clients_router.post("/login")
def login(clients:Login, db:Session=Depends(get_db)):
    login=Clients(
        email=clients.email,
        password=clients.password
    ) 
    db.add(login)
    db.commit()
    db.refresh(login)
    return login

@clients_router.post("/create")
def add_clients(clients: ClientsCreate, db: Session = Depends(get_db)):
    new_clients = Clients(
        clients_id=clients.clients_id,
        name=clients.name,
        email=clients.email,
        password=clients.password,
        role=clients.role,
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

@clients_router.put("/updateClients/{clients_id}")
def update_clients(clients_id:int , clients:ClientUpdate, db:Session=Depends(get_db)):
    update_clients=db.query(Clients).filter(Clients.clients_id==clients_id).first()
    if update_clients:
        update_clients.name=clients.name
        update_clients.email=clients.email
        update_clients.role=clients.role
        update_clients.age=clients.age
        update_clients.phone_number=clients.phone_number
        update_clients.language=clients.language
        update_clients.address=clients.address
        db.commit()
        db.refresh(update_clients)
        db.close()
        return update_clients
    return {"message": "Clients not found"}

@clients_router.delete("/deleteClients/{clients_id}")
def delete_clients(clients_id:int , db:Session=Depends(get_db)):
    delete_clients=db.query(Clients).filter(Clients.clients_id==clients_id).first()
    if delete_clients:
        db.delete(delete_clients)
        db.commit()
        return {"message": "Clients deleted successfully"}
    return {"message": "Clients not found"}
        


