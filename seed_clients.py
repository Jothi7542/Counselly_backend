from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.clients import Clients
from models.appointments import Appointments
from models.counsellors import Counsellors
from auth_utils import get_password_hash
from datetime import date
import os

DATABASE_URL = "postgresql+psycopg2://postgres:AcademyRootPassword@localhost:5432/counselly"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    # 1. Find a counsellor
    counsellor = db.query(Counsellors).first()
    if not counsellor:
        print("No counsellor found to associate clients with.")
    else:
        print(f"Found counsellor: {counsellor.name} (ID: {counsellor.counsellors_id})")

        # 2. Create two clients
        client1 = Clients(
            name="Meera",
            email="meera@example.com",
            password=get_password_hash("password123"),
            role="client",
            age=25,
            gender="Female"
        )
        client2 = Clients(
            name="Kaviya",
            email="kaviya@example.com",
            password=get_password_hash("password123"),
            role="client",
            age=28,
            gender="Female"
        )
        db.add(client1)
        db.add(client2)
        db.commit()
        db.refresh(client1)
        db.refresh(client2)
        print(f"Created clients: {client1.name}, {client2.name}")

        # 3. Create two appointments
        app1 = Appointments(
            clients_id=client1.clients_id,
            counsellors_id=counsellor.counsellors_id,
            availability_id=1, # Assuming some availability exists or just bypass FK if allowed (checks schema)
            date=date(2026, 2, 10),
            time="10:00 AM",
            mode="online",
            session_period="morning",
            therapy_type="Individual",
            reason="Stress",
            status="completed",
            counsellor_response="accepted"
        )
        app2 = Appointments(
            clients_id=client2.clients_id,
            counsellors_id=counsellor.counsellors_id,
            availability_id=1,
            date=date(2026, 2, 11),
            time="11:00 AM",
            mode="in_person",
            session_period="morning",
            therapy_type="Individual",
            reason="Anxiety",
            status="booked",
            counsellor_response="accepted"
        )
        db.add(app1)
        db.add(app2)
        db.commit()
        print("Created appointments for these clients.")

finally:
    db.close()
