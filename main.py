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

# 🔹 Create tables
Base.metadata.create_all(bind=engine)

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

