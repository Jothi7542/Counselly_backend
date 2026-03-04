from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.counsellors import Counsellors
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"DATABASE_URL from .env: {DATABASE_URL}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    print("--- FULL COUNSELLOR DUMP ---")
    all_c = db.query(Counsellors).order_by(Counsellors.counsellors_id).all()
    print(f"Total: {len(all_c)}")
    for c in all_c:
        print(f"ID: {c.counsellors_id} | Name: {c.name} | Email: {c.email} | Status: {c.status}")
finally:
    db.close()
