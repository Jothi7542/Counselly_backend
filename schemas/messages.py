from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    sender_id: int
    sender_role: str
    receiver_id: int
    receiver_role: str
    content: str
    message_type: str = "text"   

class MessageResponse(BaseModel):
    message_id: int
    sender_id: int
    sender_role: str
    receiver_id: int
    receiver_role: str
    content: str
    message_type: str
    is_read: bool
    timestamp: datetime