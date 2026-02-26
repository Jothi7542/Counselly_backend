from sqlalchemy import create_engine, inspect
import os

DATABASE_URL = "postgresql+psycopg2://postgres:AcademyRootPassword@localhost:5432/counselly"
engine = create_engine(DATABASE_URL)

def check_reviews_schema():
    inspector = inspect(engine)
    columns = inspector.get_columns('reviews')
    print("Columns in 'reviews' table:")
    for column in columns:
        print(f" - {column['name']}: {column['type']}")

if __name__ == "__main__":
    try:
        check_reviews_schema()
    except Exception as e:
        print(f"Error: {e}")
