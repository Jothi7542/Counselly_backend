from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://postgres:AcademyRootPassword@localhost:5432/counselly"
engine = create_engine(DATABASE_URL)

def check_reviews_data():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT review_id, clients_id, counsellors_id, appointment_id, rating FROM reviews LIMIT 5;"))
        rows = result.fetchall()
        print(f"Reviews Data (First 5):")
        for row in rows:
            print(f" - ID: {row[0]}, Client: {row[1]}, Counsellor: {row[2]}, Appointment: {row[3]}, Rating: {row[4]}")

if __name__ == "__main__":
    try:
        check_reviews_data()
    except Exception as e:
        print(f"Error: {e}")
