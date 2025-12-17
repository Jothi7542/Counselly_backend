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
    name: str 
    email:str
    role: str 
    age: int 
    phone_number: str
    language:List[str]
    status: str 
    address:str

class Signup(BaseModel):
    name: str
    email: str
    password: str
    role: str
    age: int
    gender: str
    phone_number: str
    language:List[str]
    address:str

class Login(BaseModel):
    email: str
    password: str