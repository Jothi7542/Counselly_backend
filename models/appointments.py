from sqlalchemy import Column, Integer, String, Date, ForeignKey
from db.database import Base
from sqlalchemy.orm import relationship

class Appointments(Base):
    __tablename__="appointments"

    appointment_id=Column(Integer ,  primary_key=True, index=True)
    clients_id = Column(Integer, ForeignKey("clients.clients_id"), nullable=False)          
    counsellors_id = Column(Integer, ForeignKey("counsellors.counsellors_id"), nullable=False)  
    date = Column(Date)
    time = Column(String)
    status = Column(String)

    clients=relationship("Clients")
    counsellors=relationship("Counsellors")