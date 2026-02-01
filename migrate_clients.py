from db.database import engine
from sqlalchemy import text

def add_profile_image_to_clients():
    with engine.connect() as connection:
        try:
            connection.execute(text("ALTER TABLE clients ADD COLUMN profile_image VARCHAR"))
            print("Successfully added profile_image column to clients table.")
        except Exception as e:
            print(f"Column might already exist or error: {e}")

if __name__ == "__main__":
    add_profile_image_to_clients()
