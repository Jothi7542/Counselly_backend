from sqlalchemy import Column, Integer, String, Date ,JSON
from db.database import Base
from dependencies import utcnow
class Counsellors(Base):
    __tablename__="counsellors"

    counsellors_id=Column(Integer ,  primary_key=True, index=True)
    name=Column(String)
    email=Column(String , unique=True, index=True)
    password=Column(String)
    role=Column(String)
    age=Column(Integer)
    gender=Column(String)
    phone_number=Column(String)
    specialization=Column(String)
    experience=Column(Integer)
    expertise=Column(JSON)
    mode=Column(JSON)
    about=Column(String)
    speaks=Column(JSON)
    profile_image = Column(String)
    availability= Column(String, default="available")
    slot=Column(JSON)
    status = Column(String, default="active")
    address = Column(String)
    created_at=Column(Date , default=utcnow)  