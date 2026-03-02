from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.counsellors import Counsellors
import os

DATABASE_URL = "postgresql+psycopg2://postgres:AcademyRootPassword@localhost:5432/counselly"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    email = "yuva@counselly.com"
    counsellor = db.query(Counsellors).filter(Counsellors.email == email).first()
    if counsellor:
        print(f"Found counsellor: {counsellor.name}")
        print(f"Email: {counsellor.email}")
        print(f"Password (hashed): {counsellor.password}")
        print(f"Status: {counsellor.status}")
        print(f"Role: {counsellor.role}")
    else:
        print(f"Counsellor with email {email} not found.")

    # List all counsellors to see what's there
    all_c = db.query(Counsellors).all()
    print(f"\nTotal Counsellors: {len(all_c)}")
    for c in all_c:
        print(f" - {c.email} ({c.name}) - Status: {c.status}")

finally:
    db.close()
