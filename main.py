from fastapi import FastAPI
from db.database import Base , engine 
from routers.clients import clients_router
from routers.counsellors import counsellors_router
# from models.counsellors import Counsellors
from routers.appointments import appointments_router
from routers.messages import messages_router
from routers.reviews import reviews_router   

Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(clients_router)
app.include_router(counsellors_router)
app.include_router(appointments_router)
app.include_router(messages_router)
app.include_router(reviews_router)

@app.get("/")
def home():
    return {"message": "API Running"}

