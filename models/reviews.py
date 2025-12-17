from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, func
from db.database import Base

class Reviews(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True)

    clients_id = Column(Integer, ForeignKey("clients.clients_id"), nullable=False)
    counsellors_id = Column(Integer, ForeignKey("counsellors.counsellors_id"), nullable=False)

    rating = Column(Integer, nullable=False)
    comments = Column(String)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

