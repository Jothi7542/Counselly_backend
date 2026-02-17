from fastapi import APIRouter , Depends ,HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models.counsellors import Counsellors
from schemas.counsellors import CounsellorsCreate,CounsellorsUpdate,Signup,Login , CounsellorsResponse, TokenResponse
from auth_utils import get_password_hash, verify_password, create_access_token
from typing import List
from datetime import date
from sqlalchemy import distinct
from sqlalchemy import func
from models.appointments import Appointments
from models.clients import Clients
from models.appointments import AppointmentStatus
from models.availability import Availability
from models.reviews import Reviews


counsellors_router=APIRouter(
    prefix="/counsellors",
    tags=["Counsellors"]
)

@counsellors_router.post("/signup", response_model=TokenResponse)
def signup(counsellors: Signup, db: Session = Depends(get_db)):
    new_counsellor = Counsellors(
        name=counsellors.name,
        email=counsellors.email,
        password=get_password_hash(counsellors.password),
        role="counsellor",
        age=counsellors.age,
        gender=counsellors.gender,
        phone_number=counsellors.phone_number,
        speaks=counsellors.speaks,
        experience=counsellors.experience,
        address=counsellors.address,
    )
    db.add(new_counsellor)
    db.commit()
    db.refresh(new_counsellor)
    
    access_token = create_access_token(data={"sub": new_counsellor.email, "role": "counsellor"})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": new_counsellor
    }

@counsellors_router.post("/login", response_model=TokenResponse)
def login(data: Login, db: Session = Depends(get_db)):
    counsellor = db.query(Counsellors).filter(Counsellors.email == data.email).first()

    if not counsellor or not verify_password(data.password, counsellor.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": counsellor.email, "role": "counsellor"})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": counsellor
    }


@counsellors_router.post("/create")
def add_counsellors(counsellors: CounsellorsCreate, db: Session = Depends(get_db)):
    new_counsellors = Counsellors(
        counsellors_id=counsellors.counsellors_id,
        name=counsellors.name,
        email=counsellors.email,
        password=get_password_hash(counsellors.password),
        age=counsellors.age,
        gender=counsellors.gender,
        phone_number=counsellors.phone_number,
        specialization=counsellors.specialization,
        experience=counsellors.experience,
        expertise=counsellors.expertise,
        mode=counsellors.mode,
        about=counsellors.about,
        speaks=counsellors.speaks,
        profile_image=counsellors.profile_image,
        status=counsellors.status,
        address=counsellors.address,
        created_at=counsellors.created_at
    )
    db.add(new_counsellors)
    db.commit()
    db.refresh(new_counsellors)
    return new_counsellors


@counsellors_router.get("/", response_model=List[CounsellorsResponse])
def all_counsellors(db: Session = Depends(get_db)):
    results = db.query(
        Counsellors,
        func.count(Reviews.review_id).label("reviews_count"),
        func.coalesce(func.avg(Reviews.rating), 0).label("rating")
    ).outerjoin(Reviews, Reviews.counsellors_id == Counsellors.counsellors_id)\
     .group_by(Counsellors.counsellors_id)\
     .all()

    counsellors_list = []
    for counsellor, reviews_count, rating in results:
        # Convert model to dict to inject calculated fields
        c_dict = {c.name: getattr(counsellor, c.name) for c in counsellor.__table__.columns}
        c_dict["reviews_count"] = reviews_count
        c_dict["rating"] = round(rating, 1)
        counsellors_list.append(c_dict)

    return counsellors_list

@counsellors_router.get("/search", response_model=List[CounsellorsResponse])
def search_counsellors(
    name: str | None = None,
    specialization: str | None = None,
    mode: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(
        Counsellors,
        func.count(Reviews.review_id).label("reviews_count"),
        func.coalesce(func.avg(Reviews.rating), 0).label("rating")
    ).outerjoin(Reviews, Reviews.counsellors_id == Counsellors.counsellors_id)

    if name:
        query = query.filter(Counsellors.name.ilike(f"%{name}%"))
    if specialization:
        query = query.filter(Counsellors.specialization.ilike(f"%{specialization}%"))
    if mode:
        query = query.filter(Counsellors.mode.contains([mode]))

    results = query.group_by(Counsellors.counsellors_id).all()

    counsellors_list = []
    for counsellor, reviews_count, rating in results:
        c_dict = {c.name: getattr(counsellor, c.name) for c in counsellor.__table__.columns}
        c_dict["reviews_count"] = reviews_count
        c_dict["rating"] = round(rating, 1)
        counsellors_list.append(c_dict)

    return counsellors_list

@counsellors_router.get("/{counsellor_id}", response_model=CounsellorsResponse)
def counsellors_id(counsellor_id:int , db:Session=Depends(get_db)):
    already_counsellors=db.query(Counsellors).filter(Counsellors.counsellors_id==counsellor_id).first()
    return already_counsellors

@counsellors_router.put("/update/{counsellors_id}")
def update_counsellor(
    counsellors_id: int,
    data: CounsellorsUpdate,
    db: Session = Depends(get_db)
):
    counsellor = db.query(Counsellors).filter(
        Counsellors.counsellors_id == counsellors_id
    ).first()

    if not counsellor:
        return {"message": "Counsellor not found"}

    update_data = data.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])

    for field, value in update_data.items():
        setattr(counsellor, field, value)

    db.commit()
    db.refresh(counsellor)
    return counsellor

@counsellors_router.delete("/deleteCounsellors/{counsellor_id}")
def delete_counsellor(
    counsellor_id: int,
    db: Session = Depends(get_db)
):
    counsellor = db.query(Counsellors).filter(
        Counsellors.counsellors_id == counsellor_id
    ).first()

    if not counsellor:
        raise HTTPException(status_code=404, detail="Counsellor not found")

   
    db.query(Availability).filter(
        Availability.counsellors_id == counsellor_id
    ).delete()

    db.query(Reviews).filter(
        Reviews.counsellors_id == counsellor_id
    ).delete()

  
    db.delete(counsellor)
    db.commit()

    return {"message": "Counsellor deleted successfully"}



@counsellors_router.get("/{counsellor_id}/stats")
def counsellor_stats(counsellor_id: int, db: Session = Depends(get_db)):
    today = date.today()

    total_sessions = db.query(Appointments).filter(
        Appointments.counsellors_id == counsellor_id
    ).count()

    upcoming_sessions = db.query(Appointments).filter(
        Appointments.counsellors_id == counsellor_id,
        Appointments.status == "booked",
        Appointments.date >= today
    ).count()

    total_clients = db.query(
        distinct(Appointments.clients_id)
    ).filter(
        Appointments.counsellors_id == counsellor_id
    ).count()


    return {
        "total_sessions": total_sessions,
        "upcoming_sessions": upcoming_sessions,
        "total_clients": total_clients
    }
@counsellors_router.get("/{counsellor_id}/upcoming-sessions")
def upcoming_sessions(counsellor_id: int, db: Session = Depends(get_db)):

    return (
        db.query(
            Appointments.date,
            Appointments.time,
            Clients.name.label("client_name"),
            Appointments.mode,
            Appointments.counsellor_response
        )
        .join(Clients, Clients.clients_id == Appointments.clients_id)
        .filter(
            Appointments.counsellors_id == counsellor_id,
            Appointments.status == AppointmentStatus.booked.value
        )
        .all()
    )


@counsellors_router.get("/{counsellor_id}/clients")
def get_counsellor_clients(counsellor_id: int, db: Session = Depends(get_db)):
    # Join Appointments and Clients to get unique clients who have booked with this counsellor
    results = (
        db.query(
            Clients.name,
            func.count(Appointments.appointment_id).label("total_sessions"),
            func.max(Appointments.date).label("last_session")
        )
        .join(Appointments, Clients.clients_id == Appointments.clients_id)
        .filter(Appointments.counsellors_id == counsellor_id)
        .group_by(Clients.clients_id, Clients.name)
        .all()
    )

    return [
        {
            "name": name,
            "total_sessions": total_sessions,
            "last_session": last_session,
            "status": "Active"
        }
        for name, total_sessions, last_session in results
    ]

@counsellors_router.get("/{counsellor_id}/card")
def counsellor_card(counsellor_id: int, db: Session = Depends(get_db)):

    counsellor = db.query(Counsellors).filter(
        Counsellors.counsellors_id == counsellor_id
    ).first()

    if not counsellor:
        raise HTTPException(status_code=404, detail="Counsellor not found")

    # ⭐ rating & reviews
    review_stats = db.query(
        func.count(Reviews.id).label("reviews_count"),
        func.coalesce(func.avg(Reviews.rating), 0).label("avg_rating")
    ).filter(
        Reviews.counsellors_id == counsellor_id
    ).first()

    return {
        "name": counsellor.name,
        "profile_image": counsellor.profile_image,
        "experience": f"{counsellor.experience} years of experience",
        "rating": round(review_stats.avg_rating, 1),
        "reviews_count": review_stats.reviews_count,
        "speaks": counsellor.speaks,
        "mode": counsellor.mode,
        "expertise": counsellor.expertise
    }