from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.counsellors import Counsellors
import os

DATABASE_URL = "postgresql+psycopg2://postgres:AcademyRootPassword@localhost:5432/counselly"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    print("--- CHECKING SPECIFIC IDs ---")
    ids_to_check = [9, 20, 70, 71, 75]
    for cid in ids_to_check:
        c = db.query(Counsellors).filter(Counsellors.counsellors_id == cid).first()
        if c:
            print(f"ID {cid}: Found {c.name} ({c.email})")
        else:
            print(f"ID {cid}: NOT FOUND")
            
finally:
    db.close()
