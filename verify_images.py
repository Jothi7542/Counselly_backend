from db.database import SessionLocal
from models.counsellors import Counsellors

def verify_images():
    db = SessionLocal()
    counsellors = db.query(Counsellors).all()
    with open("verification_result.txt", "w") as f:
        f.write(f"{'Name':<15} | {'Profile Image':<40} | {'Email'}\n")
        f.write("-" * 80 + "\n")
        for c in counsellors:
            f.write(f"{c.name:<15} | {c.profile_image:<40} | {c.email}\n")
    db.close()

if __name__ == "__main__":
    verify_images()
