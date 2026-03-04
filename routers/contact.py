from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models.contact import ContactMessage
from schemas.contact import ContactCreate, ContactResponse
from typing import List

contact_router = APIRouter(
    prefix="/contact",
    tags=["Contact"]
)

@contact_router.post("/submit", response_model=ContactResponse)
def submit_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    try:
        new_msg = ContactMessage(
            name=contact.name,
            email=contact.email,
            message=contact.message
        )
        db.add(new_msg)
        db.commit()
        db.refresh(new_msg)
        return new_msg
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@contact_router.get("/all", response_model=List[ContactResponse])
def get_contact_messages(db: Session = Depends(get_db)):
    # This should be protected by admin role in a real scenario
    messages = db.query(ContactMessage).order_by(ContactMessage.created_at.desc()).all()
    return messages
