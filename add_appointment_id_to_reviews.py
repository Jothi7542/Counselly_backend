from sqlalchemy import text
from db.database import SessionLocal

def update_schema():
    print("🚀 Updating database schema for reviews...")
    db = SessionLocal()
    try:
        # Check if 'appointment_id' column exists in 'reviews' table
        check_query = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='reviews' AND column_name='appointment_id';
        """)
        
        result = db.execute(check_query).fetchone()
        
        if not result:
            print("❌ 'appointment_id' column is missing. Adding it now...")
            # Add the 'appointment_id' column
            add_query = text("ALTER TABLE reviews ADD COLUMN appointment_id INTEGER REFERENCES appointments(appointment_id);")
            db.execute(add_query)
            db.commit()
            print("✅ 'appointment_id' column added successfully!")
        else:
            print("✅ 'appointment_id' column already exists.")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_schema()
