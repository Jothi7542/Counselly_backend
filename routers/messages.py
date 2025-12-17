from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models.messages import Messages
from schemas.messages import MessageCreate, MessageResponse
from typing import List

messages_router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)

@messages_router.post("/create", response_model=MessageResponse)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    new_message = Messages(
        sender_id=message.sender_id,
        sender_role=message.sender_role,
        receiver_id=message.receiver_id,
        receiver_role=message.receiver_role,
        content=message.content,
        message_type=message.message_type
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


@messages_router.get("/all", response_model=List[MessageResponse])
def get_all_messages(db: Session = Depends(get_db)):
    all_messages = db.query(Messages).all()
    db.close()
    return all_messages


@messages_router.get("/{message_id}", response_model=MessageResponse)
def get_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Messages).filter(Messages.message_id == message_id).first()
    if not message:
        db.close()
        raise HTTPException(status_code=404, detail="Message not found")
    db.close()
    return message


@messages_router.put("/{message_id}", response_model=MessageResponse)
def mark_message_read(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Messages).filter(Messages.message_id == message_id).first()
    if not message:
        db.close()
        raise HTTPException(status_code=404, detail="Message not found")
    message.is_read = True
    db.commit()
    db.refresh(message)
    db.close()
    return message


@messages_router.delete("/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Messages).filter(Messages.message_id == message_id).first()
    if not message:
        db.close()
        return {"message": "Message not found"}
    db.delete(message)
    db.commit()
    db.close()
    return {"message": "Message deleted successfully"}

