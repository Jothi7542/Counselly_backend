from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base
from datetime import datetime

class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    message = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, reviewed, archived
    created_at = Column(DateTime, default=datetime.utcnow)
