from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.counsellors import Counsellors
import os

DATABASE_URL = "postgresql+psycopg2://postgres:AcademyRootPassword@localhost:5432/counselly"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    all_c = db.query(Counsellors).order_by(Counsellors.name).all()
    print(f"TOTAL: {len(all_c)}")
    for c in all_c:
        print(f"Name: [{c.name}] | Email: [{c.email}] | Role: [{c.role}] | Status: [{c.status}]")
finally:
    db.close()
