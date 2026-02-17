from sqlalchemy import Column, Integer, Date, String, Boolean, ForeignKey, JSON
from db.database import Base

class Availability(Base):
    __tablename__ = "availability"

    availability_id = Column(Integer, primary_key=True, index=True)
    counsellors_id = Column(Integer, ForeignKey("counsellors.counsellors_id"))
    
    date = Column(Date, nullable=False)
    # day = Column(String, nullable=False)      
    # month = Column(String, nullable=False)
    time_slot = Column(String, nullable=False)  
    session_period = Column(String, nullable=False)

    is_booked = Column(Boolean, default=False)

