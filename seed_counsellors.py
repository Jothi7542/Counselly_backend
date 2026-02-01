import sys
import os
from datetime import date, timedelta
from dotenv import load_dotenv

sys.path.append('c:/Jothi/Projects/F&B/Counselly_FastAPI')
load_dotenv('c:/Jothi/Projects/F&B/Counselly_FastAPI/.env')

from db.database import SessionLocal, engine
from models.counsellors import Counsellors, Base
from models.availability import Availability
from models.appointments import Appointments
from models.clients import Clients
from models.reviews import Reviews
from sqlalchemy import text
from utils.auth import hash_password

Base.metadata.create_all(bind=engine)

def seed_data():
    session = SessionLocal()
    try:
        # Clear existing using raw SQL to ensure order and avoid mapper issues
        with engine.connect() as connection:
            transaction = connection.begin()
            try:
                connection.execute(text("DELETE FROM reviews"))
                connection.execute(text("DELETE FROM appointments"))
                connection.execute(text("DELETE FROM clients"))
                connection.execute(text("DELETE FROM availability"))
                connection.execute(text("DELETE FROM counsellors"))
                transaction.commit()
            except Exception as e:
                transaction.rollback()
                raise e

        counsellors_data = [
            {"name": "Akshaya", "specialization": "Counselling Psychologist", "experience": "3.5", "profile_image": "../Assets/Wireframep1.webp", "email": "akshaya@counselly.com", "password": "Akshaya@2025", "about": "I specialize in addressing anxiety, depression, and self-esteem issues through a compassionate, client-centered approach."},
            {"name": "Meera", "specialization": "Clinical Psychologist", "experience": "5", "profile_image": "../Assets/wireframep2.webp", "email": "meera@counselly.com", "password": "Meera@2025", "about": "With a background in clinical psychology, I help individuals navigate complex trauma and emotional regulation challenges."},
            {"name": "Priya", "specialization": "Child Psychologist", "experience": "2", "profile_image": "../Assets/wire6.webp", "email": "priya@counselly.com", "password": "Priya@2025", "about": "I focus on child developmental needs and family dynamics, providing a safe space for young minds to express themselves."},
            {"name": "Samikshaa", "specialization": "Trauma Expert", "experience": "4", "profile_image": "../Assets/wire7.webp", "email": "sam@counselly.com", "password": "Sam@2025", "about": "My expertise lies in trauma-informed care, helping clients rebuild resilience after difficult life experiences."},
            {"name": "Ashwini", "specialization": "Family Therapist", "experience": "6", "profile_image": "../Assets/wire8.webp", "email": "ashwini@counselly.com", "password": "Ashwini@2025", "about": "I facilitate healthy communication within families and couples, resolving conflicts with empathy and professional guidance."},
            {"name": "Jai shree", "specialization": "Career Coach", "experience": "3", "profile_image": "../Assets/wire9.webp", "email": "jai@counselly.com", "password": "Jai@2025", "about": "I guide professionals and students through career transitions, helping them align their goals with their personal values."},
            {"name": "Kaviya", "specialization": "Mental Wellness", "experience": "2.5", "profile_image": "../Assets/wire10.webp", "email": "kaviya@counselly.com", "password": "Kaviya@2025", "about": "Dedicated to holistic wellness, I provide tools for stress management and mindfulness to improve daily quality of life."},
            {"name": "Sridevi", "specialization": "Behavioral Therapist", "experience": "7", "profile_image": "../Assets/wire5.webp", "email": "sridevi@counselly.com", "password": "Sridevi@2025", "about": "Specializing in behavioral patterns, I help clients develop positive habits and overcome deep-seated emotional barriers."},
            {"name": "Yuvasree", "specialization": "Holistic Healing", "experience": "4.5", "profile_image": "../Assets/Wire4.webp", "email": "yuva@counselly.com", "password": "Yuvasree@2025", "about": "I integrate traditional counselling with holistic practices to provide a well-rounded approach to mental health and peace."}
        ]

        inserted_counsellors = []
        for data in counsellors_data:
            c = Counsellors(
                name=data["name"],
                email=data["email"],
                password=hash_password(data["password"]), # Unique Hashed Password
                specialization=data["specialization"],
                experience=data["experience"],
                profile_image=data["profile_image"],
                expertise=["Anxiety", "Depression"],
                speaks=["English", "Tamil"],
                mode=["Online", "In Person"],
                address="Chennai, India",
                about=data.get("about", f"I am {data['name']}, a passionate {data['specialization']} with over {data['experience']} years of experience.")
            )
            session.add(c)
            session.flush()
            inserted_counsellors.append(c)

        # Seed some availability for the next 3 days
        today = date.today()
        for c in inserted_counsellors:
            for i in range(3):
                target_date = today + timedelta(days=i)
                # Morning slots
                session.add(Availability(
                    counsellors_id=c.counsellors_id,
                    date=target_date,
                    day=target_date.strftime("%A"),
                    month=target_date.strftime("%B"),
                    time_slot="09:00 AM",
                    session_period="morning"
                ))
                session.add(Availability(
                    counsellors_id=c.counsellors_id,
                    date=target_date,
                    day=target_date.strftime("%A"),
                    month=target_date.strftime("%B"),
                    time_slot="10:30 AM",
                    session_period="morning"
                ))
                # Afternoon
                session.add(Availability(
                    counsellors_id=c.counsellors_id,
                    date=target_date,
                    day=target_date.strftime("%A"),
                    month=target_date.strftime("%B"),
                    time_slot="02:00 PM",
                    session_period="afternoon"
                ))

        # Create a dummy client to author the reviews
        dummy_client = Clients(
            name="Anonymous User",
            email="anonymous@counselly.com",
            password=hash_password("password"),
            age=25,
            gender="Other",
            phone_number="0000000000"
        )
        session.add(dummy_client)
        session.flush()

        import random
        review_comments = [
            "Very helpful session!", "Highly recommended.", "Great listener and very professional.",
            "I felt understood.", "Amazing experience.", "Helped me a lot with my anxiety.",
            "Kind and patient.", "Best counsellor I've met."
        ]

        for c in inserted_counsellors:
            # Seed 3 to 8 reviews per counsellor
            num_reviews = random.randint(3, 8)
            for _ in range(num_reviews):
                rating = random.choice([4, 5, 5, 4, 5]) # Mostly good ratings
                session.add(Reviews(
                    clients_id=dummy_client.clients_id,
                    counsellors_id=c.counsellors_id,
                    rating=rating,
                    comments=random.choice(review_comments)
                ))
        
        session.commit()
        print(f"Seeded 9 unique counsellors and 100+ availability slots.")
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    seed_data()
