from fastapi.testclient import TestClient
from main import app
from db.database import SessionLocal
from models.counsellors import Counsellors
from models.clients import Clients
from models.availability import Availability
from utils.auth import hash_password
from datetime import date

client = TestClient(app)

def verify_stats_update():
    db = SessionLocal()
    
    # 1. Setup: Get a counsellor and a specific slot
    akshaya = db.query(Counsellors).filter(Counsellors.email == "akshaya@counselly.com").first()
    if not akshaya:
        print("Akshaya not found!")
        return

    # Create a test client
    test_client = db.query(Clients).filter(Clients.email == "stats_test@user.com").first()
    if not test_client:
        test_client = Clients(
            name="Stats Tester",
            email="stats_test@user.com",
            password=hash_password("password"),
            age=30,
            gender="Male",
            phone_number="1234567890"
        )
        db.add(test_client)
        db.commit()
        db.refresh(test_client)

    # Find a free slot
    slot = db.query(Availability).filter(
        Availability.counsellors_id == akshaya.counsellors_id,
        Availability.is_booked == False
    ).first()
    
    if not slot:
        print("No free slots available for Akshaya to test booking.")
        return

    print(f"Testing with Counsellor: {akshaya.name} (ID: {akshaya.counsellors_id})")
    
    # 2. Get Initial Stats
    response = client.get(f"/counsellors/{akshaya.counsellors_id}/stats")
    initial_stats = response.json()
    print(f"Initial Stats: {initial_stats}")

    # 3. Make a Booking
    booking_data = {
        "clients_id": test_client.clients_id,
        "counsellors_id": akshaya.counsellors_id,
        "availability_id": slot.availability_id,
        "mode": "online",
        "address": "test address",
        "therapy_type": "Individual",
        "reason": "Testing stats"
    }
    
    print("Booking appointment...")
    response = client.post("/appointments/new_appointment", json=booking_data)
    if response.status_code != 200:
        print(f"Booking failed: {response.text}")
        return
    
    # 4. Get New Stats
    response = client.get(f"/counsellors/{akshaya.counsellors_id}/stats")
    new_stats = response.json()
    print(f"New Stats: {new_stats}")

    # 5. Verify Changes
    print("\n--- Verification ---")
    
    sessions_increased = new_stats['total_sessions'] == initial_stats['total_sessions'] + 1
    upcoming_increased = new_stats['upcoming_sessions'] == initial_stats['upcoming_sessions'] + 1
    
    # Client count increases only if this client hasn't booked before
    # Since we reused or created a specific test client, we can't strict check client count if they booked before.
    # But total sessions MUST increase.
    
    print(f"Total Sessions Increased: {sessions_increased} ({initial_stats['total_sessions']} -> {new_stats['total_sessions']})")
    print(f"Upcoming Sessions Increased: {upcoming_increased} ({initial_stats['upcoming_sessions']} -> {new_stats['upcoming_sessions']})")

    if sessions_increased and upcoming_increased:
        print("SUCCESS: Stats updated correctly.")
    else:
        print("FAILURE: Stats did not update as expected.")

if __name__ == "__main__":
    verify_stats_update()
