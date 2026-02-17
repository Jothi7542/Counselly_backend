import sys
import os

# Add the current directory to sys.path to find local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.database import SessionLocal
from models.counsellors import Counsellors
from models.clients import Clients
from models.reviews import Reviews
import random

def seed_reviews():
    db = SessionLocal()
    try:
        counsellors = db.query(Counsellors).all()
        client = db.query(Clients).first()

        if not client:
            print("No clients found in database. Please create a client first.")
            return

        print(f"Found {len(counsellors)} counsellors. Seeding reviews...")

        reviews_data = [
            "Great experience, very helpful.",
            "Helped me through a tough time.",
            "Very professional and empathetic.",
            "I feel much better after our sessions.",
            "Highly recommend for anyone struggling with anxiety.",
            "Very patient and understanding.",
            "The sessions were very insightful.",
            "Excellent counsellor, very knowledgeable.",
            "A safe space to talk about anything.",
            "Changed my perspective on mental health."
        ]

        for counsellor in counsellors:
            # Check if counsellor already has reviews
            existing_count = db.query(Reviews).filter(Reviews.counsellors_id == counsellor.counsellors_id).count()
            if existing_count > 0:
                print(f"Counsellor {counsellor.name} already has {existing_count} reviews. Skipping.")
                continue

            num_reviews = random.randint(3, 8)
            for _ in range(num_reviews):
                rating = random.randint(4, 5)
                comments = random.choice(reviews_data)
                
                review = Reviews(
                    clients_id=client.clients_id,
                    counsellors_id=counsellor.counsellors_id,
                    rating=rating,
                    comments=comments
                )
                db.add(review)
            
            print(f"Added {num_reviews} reviews for {counsellor.name}")

        db.commit()
        print("Success: Database seeded with reviews.")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_reviews()
