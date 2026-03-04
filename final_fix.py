from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.counsellors import Counsellors
from utils.auth import hash_password
import os

DATABASE_URL = "postgresql+psycopg2://postgres:AcademyRootPassword@localhost:5432/counselly"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# Simplified list for final verification
targets = [
    {"email": "yuva@counselly.com", "pass": "Counselly@123"},
    {"email": "sam@counselly.com", "pass": "Counselly@123"},
    {"email": "ashwini@counselly.com", "pass": "Counselly@123"}
]

try:
    for t in targets:
        c = db.query(Counsellors).filter(Counsellors.email == t["email"]).first()
        if c:
            print(f"DEBUG: Setting {t['email']} password to {t['pass']}")
            c.password = hash_password(t["pass"])
            c.status = "active" # Ensure active
        else:
            print(f"DEBUG: {t['email']} NOT FOUND")
    
    db.commit()
    print("DEBUG: Final password reset complete.")

finally:
    db.close()
