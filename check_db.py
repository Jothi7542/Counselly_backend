from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.clients import Clients
from models.appointments import Appointments
import os

DATABASE_URL = "postgresql+psycopg2://postgres:AcademyRootPassword@localhost:5432/counselly"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    clients = db.query(Clients).all()
    print(f"Total Clients: {len(clients)}")
    for c in clients:
        print(f" - {c.clients_id}: {c.name}")

    appointments = db.query(Appointments).all()
    print(f"Total Appointments: {len(appointments)}")
    for a in appointments:
        print(f" - ID: {a.appointment_id}, Client: {a.clients_id}, Counsellor: {a.counsellors_id}, Status: {a.status}")

finally:
    db.close()
