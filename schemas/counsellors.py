from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CounsellorsCreate(BaseModel):
    counsellors_id: int
    name: str
    email: str
    password: str
    age: int
    gender: str
    phone_number: str
    specialization: str
    experience: str
    expertise: List[str]
    mode: List[str]
    about: str
    speaks: List[str]
    profile_image: str
    availability: str
    status: str
    address: str
    created_at:datetime

class CounsellorsUpdate(BaseModel):
    name:str
    email:str
    password:str
    age:int
    gender:str
    phone_number:str
    specialization:str
    experience:str
    expertise:List[str]
    mode:List[str]
    about:str
    speaks:List[str]
    profile_image:str
    availability:str
    address:str

class Login(BaseModel):
    email: str
    password: str

class Signup(BaseModel):
    name: str
    email: str
    password: str
    age: int
    gender: str
    phone_number: str
    speaks: List[str]
    experience: int
    address: str
    specialization: Optional[str] = "Counselling Psychologist"
    profile_image: Optional[str] = None
    about: Optional[str] = None

class CounsellorsResponse(BaseModel):
    counsellors_id: int
    name: str | None = None
    email: str | None = None
    specialization: str | None = "Counselling Psychologist"
    experience: str | None = "0"
    expertise: List[str] | None = []
    mode: List[str] | None = []
    speaks: List[str] | None = []
    status: str | None = "pending"
    profile_image: str | None = None
    about: str | None = None
    rating: float | None = 0.0
    reviews_count: int | None = 0

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: CounsellorsResponse
class CounsellorCardResponse(BaseModel):
    counsellors_id: int
    name: str
    profile_image: str | None
    experience: str              # "3.5 years of experience"
    rating: float                # ⭐⭐⭐⭐
    reviews_count: int           # (13 reviews)
    speaks: List[str]
    mode: List[str]
    expertise: List[str]
    price: int

    class Config:
        from_attributes = True
