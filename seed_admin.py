import sys
import os

# Add parent directory to path to import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import SessionLocal
from models.admins import Admins
from auth_utils import get_password_hash

def seed_admin():
    db = SessionLocal()
    try:
        # Check if admin already exists
        admin_email = "admin@counselly.com"
        existing = db.query(Admins).filter(Admins.email == admin_email).first()
        
        if existing:
            print(f"Admin {admin_email} already exists.")
            return

        new_admin = Admins(
            name="Counselly Admin",
            email=admin_email,
            password=get_password_hash("Admin@123"),
            role="admin"
        )
        db.add(new_admin)
        db.commit()
        print("Initial Admin created successfully!")
        print(f"Email: {admin_email}")
        print("Password: Admin@123")
        
    except Exception as e:
        print(f"Error seeding admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()
