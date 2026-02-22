from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base
from dependencies import utcnow

class Admins(Base):
    __tablename__ = "admins"

    admins_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="admin")
    created_at = Column(DateTime, default=utcnow)
