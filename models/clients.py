from sqlalchemy import Column, Integer, String, DateTime, JSON
from db.database import Base
from dependencies import utcnow

class Clients(Base):
    __tablename__="clients"

    clients_id=Column(Integer, primary_key=True, index=True)
    name=Column(String)
    email=Column(String , unique=True, index=True)
    password=Column(String)
    role=Column(String)
    age=Column(Integer)
    gender=Column(String)
    phone_number=Column(String)
    language=Column(JSON)
    status = Column(String, default="active")
    address = Column(String)
    created_at=Column(DateTime , default=utcnow)
    
