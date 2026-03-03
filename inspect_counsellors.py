from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.counsellors import Counsellors
import os

DATABASE_URL = "postgresql+psycopg2://postgres:AcademyRootPassword@localhost:5432/counselly"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

emails_to_check = ["yuva@counselly.com", "sam@counselly.com", "ashwini@counselly.com"]

try:
    print("--- DEEP INSPECTION ---")
    for email in emails_to_check:
        c = db.query(Counsellors).filter(Counsellors.email.ilike(email)).first()
        if c:
            print(f"Name: '{c.name}'")
            print(f"Email in DB: '{c.email}' (Length: {len(c.email)})")
            print(f"Email Hex: {c.email.encode('utf-8').hex()}")
            print(f"Role: '{c.role}'")
            print(f"Status: '{c.status}'")
            print(f"Password starts with: '{c.password[:10]}...'")
            print("-" * 20)
        else:
            print(f"Email '{email}' NOT FOUND at all.")

finally:
    db.close()
