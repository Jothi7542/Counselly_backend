from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.counsellors import Counsellors
from utils.auth import hash_password
import os

# Using the URL from .env
DATABASE_URL = "postgresql+psycopg2://postgres:AcademyRootPassword@localhost:5432/counselly"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    email = "yuva@counselly.com"
    c = db.query(Counsellors).filter(Counsellors.email == email).first()
    
    if c:
        print(f"DEBUG: Found counsellor {c.name}")
        print(f"DEBUG: Email in DB: '{c.email}'")
        print(f"DEBUG: Role: {c.role}")
        print(f"DEBUG: Status: {c.status}")
        
        # Reset password to a known value for testing
        new_pass = "Counselly@123"
        c.password = hash_password(new_pass)
        db.commit()
        print(f"DEBUG: Password reset to '{new_pass}' for {email}")
    else:
        print(f"DEBUG: Counsellor {email} NOT FOUND in database.")
        
        # List all counsellors to see what we have
        all_c = db.query(Counsellors).all()
        print(f"DEBUG: Total counsellors in DB: {len(all_c)}")
        for x in all_c:
            print(f" - ID: {x.counsellors_id}, Name: {x.name}, Email: '{x.email}'")

finally:
    db.close()
