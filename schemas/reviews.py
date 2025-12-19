from pydantic import BaseModel
from datetime import datetime
# from typing import Optional

class ReviewCreate(BaseModel):
    clients_id: int
    counsellors_id: int
    rating: int
    comments: str 


class ReviewResponse(BaseModel):
    review_id: int
    clients_id: int
    counsellors_id: int
    rating: int
    comments: str 
    is_active:bool
    created_at: datetime

class ReviewUpdate(BaseModel):
    rating:int
    comments:str

class Config:
    from_attributes = True