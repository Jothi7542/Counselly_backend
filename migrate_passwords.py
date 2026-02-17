from db.database import SessionLocal
from models.clients import Clients
from models.counsellors import Counsellors
from auth_utils import get_password_hash

def migrate_passwords():
    db = SessionLocal()
    try:
        # Migrate Clients
        clients = db.query(Clients).all()
        print(f"Checking {len(clients)} clients...")
        for client in clients:
            # Check if already hashed (bcrypt hashes start with $2b$ or $2a$)
            if not client.password.startswith("$2b$"):
                print(f"Hashing password for client: {client.email}")
                client.password = get_password_hash(client.password)
        
        # Migrate Counsellors
        counsellors = db.query(Counsellors).all()
        print(f"Checking {len(counsellors)} counsellors...")
        for counsellor in counsellors:
            if not counsellor.password.startswith("$2b$"):
                print(f"Hashing password for counsellor: {counsellor.email}")
                counsellor.password = get_password_hash(counsellor.password)
        
        db.commit()
        print("Migration complete!")
    except Exception as e:
        print(f"Error during migration: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate_passwords()
