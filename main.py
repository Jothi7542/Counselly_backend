from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.database import Base, engine
from routers.clients import clients_router
from routers.counsellors import counsellors_router
from routers.appointments import appointments_router
from routers.messages import messages_router
from routers.reviews import reviews_router
from routers.availability import availability_router
from routers.admins import admins_router

# 🔹 Create tables & fix schema
Base.metadata.create_all(bind=engine)

# Auto-fix missing role column if it exists
try:
    from sqlalchemy import text
    from db.database import SessionLocal
    db_sync = SessionLocal()
    # Fix counsellors
    db_sync.execute(text("ALTER TABLE counsellors ADD COLUMN IF NOT EXISTS role VARCHAR DEFAULT 'counsellor';"))
    db_sync.execute(text("UPDATE counsellors SET role = 'counsellor' WHERE role IS NULL;"))
    # Fix clients
    db_sync.execute(text("ALTER TABLE clients ADD COLUMN IF NOT EXISTS role VARCHAR DEFAULT 'client';"))
    db_sync.execute(text("UPDATE clients SET role = 'client' WHERE role IS NULL;"))
    db_sync.commit()
    db_sync.close()
    print("✅ Database schema synchronized for counsellors and clients")
except Exception as e:
    print(f"⚠️ Schema sync hint: {e}")

# 🔹 FastAPI app
app = FastAPI()

# 🔥 CORS MIDDLEWARE (VERY IMPORTANT) 
origins = [
    "http://localhost:8000",
    "http://localhost:5500",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5500",
    "https://counselly-frontend.vercel.app"
]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

# 🔹 Routers
app.include_router(clients_router)
app.include_router(counsellors_router)
app.include_router(appointments_router)
app.include_router(messages_router)
app.include_router(reviews_router)
app.include_router(availability_router)
app.include_router(admins_router)

# 🔹 Health check
@app.get("/")
def home():
    return {"message": "API Running"}


# from fastapi import FastAPI
# from db.database import Base , engine 
# from routers.clients import clients_router
# from routers.counsellors import counsellors_router
# # from models.counsellors import Counsellors
# from routers.appointments import appointments_router
# from routers.messages import messages_router
# from routers.reviews import reviews_router  
# from routers.availability import availability_router 

# Base.metadata.create_all(bind=engine)

# app=FastAPI()

# app.include_router(clients_router)
# app.include_router(counsellors_router)
# app.include_router(appointments_router)
# app.include_router(messages_router)
# app.include_router(reviews_router)
# app.include_router(availability_router)

# @app.get("/")
# def home():
#     return {"message": "API Running"}

