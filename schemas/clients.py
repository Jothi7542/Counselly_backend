from pydantic import BaseModel
from typing import List
from datetime import datetime

class ClientsCreate(BaseModel):
    clients_id:int
    name:str
    email:str
    password:str
    role:str
    age:int
    gender:str
    phone_number:str
    language:List[str]
    status:str
    address:str
    created_at:datetime

class ClientUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    role: str | None = None
    age: int | None = None
    gender: str | None = None
    phone_number: str | None = None
    language: List[str] | None = None
    status: str | None = None
    address: str | None = None
    profile_image: str | None = None

class Signup(BaseModel):
    name: str
    email: str
    password: str
    age: int
    gender: str
    phone_number: str
    language:List[str]
    address:str
    profile_image: str | None = None

class Login(BaseModel):
    email: str
    password: str

class ClientResponse(BaseModel):
    clients_id: int
    name: str
    email: str
    role: str
    age: int
    gender: str
    phone_number: str
    language: List[str]
    address: str

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: ClientResponse