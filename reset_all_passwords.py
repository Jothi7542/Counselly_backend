from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.counsellors import Counsellors
from utils.auth import hash_password
import os

DATABASE_URL = "postgresql+psycopg2://postgres:AcademyRootPassword@localhost:5432/counselly"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# Credentials from the image
credentials = [
    {"email": "akshaya@counselly.com", "password": "Akshaya@2025"},
    {"email": "meera@counselly.com", "password": "Meera@2025"},
    {"email": "priya@counselly.com", "password": "Priya@2025"},
    {"email": "sam@counselly.com", "password": "Sam@2025"},
    {"email": "ashwini@counselly.com", "password": "Ashwini@2025"},
    {"email": "jai@counselly.com", "password": "Jai@2025"},
    {"email": "kaviya@counselly.com", "password": "Kaviya@2025"},
    {"email": "sridevi@counselly.com", "password": "Sridevi@2025"},
    {"email": "yuva@counselly.com", "password": "Yuvasree@2025"}
]

try:
    for cred in credentials:
        email = cred["email"]
        password = cred["password"]
        c = db.query(Counsellors).filter(Counsellors.email == email).first()
        if c:
            print(f"DEBUG: Updating {c.name} ({email})")
            c.password = hash_password(password)
        else:
            print(f"DEBUG: {email} NOT FOUND")

    db.commit()
    print("DEBUG: All passwords updated and changes committed.")

finally:
    db.close()
