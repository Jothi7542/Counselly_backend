import sys
import os
from sqlalchemy import text
from db.database import SessionLocal, engine

def fix_schema():
    print("🚀 Starting database schema synchronization...")
    db = SessionLocal()
    try:
        # Check if 'role' column exists in 'counsellors' table
        print("Checking for 'role' column in 'counsellors' table...")
        
        # PostgreSQL specific query to check column existence
        check_query = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='counsellors' AND column_name='role';
        """)
        
        result = db.execute(check_query).fetchone()
        
        if not result:
            print("❌ 'role' column is missing. Adding it now...")
            # Add the 'role' column with a default value
            add_query = text("ALTER TABLE counsellors ADD COLUMN role VARCHAR DEFAULT 'counsellor';")
            db.execute(add_query)
            db.commit()
            print("✅ 'role' column added successfully!")
        else:
            print("✅ 'role' column already exists.")

        # Also ensure all existing counsellors have the role set to 'counsellor'
        print("Ensuring all counsellors have a role...")
        update_query = text("UPDATE counsellors SET role = 'counsellor' WHERE role IS NULL;")
        db.execute(update_query)
        db.commit()
        print("✅ Data synchronization complete!")

    except Exception as e:
        print(f"❌ Error fixing schema: {e}")
        db.rollback()
    finally:
        db.close()
        print("🏁 Database session closed.")

if __name__ == "__main__":
    fix_schema()
