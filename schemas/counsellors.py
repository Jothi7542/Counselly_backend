from pydantic import BaseModel
from datetime import datetime
from typing import List

class CounsellorsCreate(BaseModel):
    counsellors_id: int
    name: str
    email: str
    password: str
    role: str
    age: int
    gender: str
    phone_number: str
    specialization: str
    experience: int
    expertise: List[str]
    mode: List[str]
    about: str
    speaks: List[str]
    profile_image: str
    availability: str
    slot: List[str]
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
    expertise:str
    mode:str
    about:str
    speaks:List[str]
    profile_image:str
    availability:str
    slot:List[str]
    address:str

class Login(BaseModel):
    email: str
    password: str

class Signup(BaseModel):
    name: str
    email: str
    password: str
    role: str
    age: int
    gender: str
    phone_number: str
    speaks: List[str]
    specialization: str
    experience: int
    expertise: str
    mode: List[str]
    about: str
    address: str
    profile_image: str 


class CounsellorsResponse(BaseModel):
    counsellors_id: int
    name: str
    email: str
    specialization: str
    experience: int
    expertise: List[str]
    mode: List[str]
    speaks: List[str]
    status: str

    class Config:
        from_attributes = True