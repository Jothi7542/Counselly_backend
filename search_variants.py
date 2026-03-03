from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.counsellors import Counsellors
import os

DATABASE_URL = "postgresql+psycopg2://postgres:AcademyRootPassword@localhost:5432/counselly"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    print("--- SEARCH BY NAME VARIANTS ---")
    variants = ["Yuva", "Sam", "Ashw"]
    for v in variants:
        results = db.query(Counsellors).filter(Counsellors.name.ilike(f"%{v}%")).all()
        print(f"Results for '{v}':")
        for c in results:
            print(f" - {c.name} ({c.email}) [ID: {c.counsellors_id}]")
            
finally:
    db.close()
