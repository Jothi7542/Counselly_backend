import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add the project root to sys.path to import models
sys.path.append(os.getcwd())

from models.counsellors import Counsellors
from db.database import SessionLocal, engine, Base
from utils.auth import hash_password

def seed_counsellors():
    db = SessionLocal()
    try:
        # Check if we already have counsellors
        count = db.query(Counsellors).count()
        if count > 0:
            print(f"Database already has {count} counsellors. Skipping seed.")
            return

        counsellors = [
            {
                "name": "Dr. Sarah Johnson",
                "email": "sarah.j@example.com",
                "password": hash_password("Password123"),
                "age": 35,
                "gender": "Female",
                "phone_number": "9876543210",
                "specialization": "Clinical Psychologist",
                "experience": "12",
                "expertise": ["Anxiety", "Depression", "CBT"],
                "mode": ["Online", "In-person"],
                "about": "Dr. Sarah has over 12 years of experience in helping people navigate complex life transitions.",
                "speaks": ["English", "Spanish"],
                "profile_image": "https://images.unsplash.com/photo-1559839734-2b71ca197ec2?auto=format&fit=crop&q=80&w=400",
                "address": "New York"
            },
            {
                "name": "Dr. Michael Chen",
                "email": "m.chen@example.com",
                "password": hash_password("Password123"),
                "age": 42,
                "gender": "Male",
                "phone_number": "9876543211",
                "specialization": "Marriage & Family Therapist",
                "experience": "15",
                "expertise": ["Relationships", "Family Therapy", "Workplace Stress"],
                "mode": ["Online"],
                "about": "Specializing in relationship dynamics and systemic family therapy.",
                "speaks": ["English", "Mandarin"],
                "profile_image": "https://images.unsplash.com/photo-1537368910025-700350fe46c7?auto=format&fit=crop&q=80&w=400",
                "address": "San Francisco"
            },
            {
                "name": "Dr. Priya Sharma",
                "email": "priya.s@example.com",
                "password": hash_password("Password123"),
                "age": 38,
                "gender": "Female",
                "phone_number": "9876543212",
                "specialization": "Child & Adolescent Specialist",
                "experience": "10",
                "expertise": ["ADHD", "Autism", "Child Psychology"],
                "mode": ["In-person"],
                "about": "Passionate about helping children reach their full potential through evidence-based play therapy.",
                "speaks": ["English", "Hindi", "Tamil"],
                "profile_image": "https://images.unsplash.com/photo-1594824476967-48c8b964273f?auto=format&fit=crop&q=80&w=400",
                "address": "Chennai"
            }
        ]

        for c_data in counsellors:
            counsellor = Counsellors(**c_data)
            db.add(counsellor)
        
        db.commit()
        print("Successfully seeded 3 counsellors into the database.")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_counsellors()
