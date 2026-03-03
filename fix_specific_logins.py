from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.counsellors import Counsellors
from utils.auth import hash_password
import os

DATABASE_URL = "postgresql+psycopg2://postgres:AcademyRootPassword@localhost:5432/counselly"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

emails_to_fix = ["yuva@counselly.com", "sam@counselly.com", "ashwini@counselly.com"]
new_pass = "Counselly@123"

try:
    for email in emails_to_fix:
        c = db.query(Counsellors).filter(Counsellors.email == email).first()
        if c:
            print(f"DEBUG: Found {c.name} ({email})")
            c.password = hash_password(new_pass)
            print(f"DEBUG: Password reset for {email}")
        else:
            print(f"DEBUG: {email} NOT FOUND")

    db.commit()
    print("DEBUG: All changes committed.")

finally:
    db.close()
