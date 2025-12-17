from sqlalchemy import Column, Integer, String, DateTime, Boolean
from db.database import Base
from dependencies import utcnow

class Messages(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, nullable=False)
    sender_role = Column(String, nullable=False)       
    receiver_id = Column(Integer, nullable=False)
    receiver_role = Column(String, nullable=False)     
    content = Column(String, nullable=False)
    message_type = Column(String, default="text")      
    is_read = Column(Boolean, default=False)            
    timestamp = Column(DateTime, default=utcnow)

