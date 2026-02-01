from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, Time
from db.database import Base
from sqlalchemy.orm import relationship
import enum

class AppointmentStatus(enum.Enum):
    booked = "booked"
    cancelled = "cancelled"
    completed = "completed"

class CounsellorResponse(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

class Mode(enum.Enum):
    online = "online"
    in_person = "in_person"

class SessionPeriod(enum.Enum):
    morning = "morning"
    afternoon = "afternoon"
    evening = "evening"

class Appointments(Base):
    __tablename__ = "appointments"

    appointment_id = Column(Integer, primary_key=True, index=True)

    clients_id = Column(Integer, ForeignKey("clients.clients_id"), nullable=False)
    counsellors_id = Column(Integer, ForeignKey("counsellors.counsellors_id"), nullable=False)
    availability_id = Column(Integer,ForeignKey("availability.availability_id"),nullable=False)


    date = Column(Date, nullable=False)
    time = Column(String, nullable=False)


    mode = Column(String, nullable=False)
    session_period = Column(String, nullable=False)
    address = Column(String, nullable=True)

    therapy_type = Column(String, nullable=False)
    reason = Column(String, nullable=False)

    status = Column(String, nullable=False)
    counsellor_response = Column(String, nullable=False)


    clients = relationship("Clients")
    counsellors = relationship("Counsellors")
    availability = relationship("Availability")
