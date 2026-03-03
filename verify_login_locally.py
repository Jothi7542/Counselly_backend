from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.counsellors import Counsellors
from utils.auth import verify_password
import os

DATABASE_URL = "postgresql+psycopg2://postgres:AcademyRootPassword@localhost:5432/counselly"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

test_cases = [
    {"email": "yuva@counselly.com", "password": "Yuvasree@2025"},
    {"email": "sam@counselly.com", "password": "Sam@2025"},
    {"email": "ashwini@counselly.com", "password": "Ashwini@2025"}
]

try:
    print("--- LOGIN SIMULATION ---")
    for test in test_cases:
        email = test["email"]
        password = test["password"]
        
        c = db.query(Counsellors).filter(Counsellors.email == email).first()
        if not c:
            print(f"FAILED: '{email}' not found")
            continue
            
        is_valid = verify_password(password, c.password)
        print(f"Login for '{email}' with password '{password}': {'SUCCESS' if is_valid else 'FAILED'}")
        
finally:
    db.close()
