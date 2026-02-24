from fastapi import APIRouter , Depends ,HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from dependencies import get_db
from models.counsellors import Counsellors
from schemas.counsellors import CounsellorsCreate,CounsellorsUpdate,Signup,Login , CounsellorsResponse, TokenResponse
from typing import List
from datetime import date
from sqlalchemy import func, or_
from models.appointments import Appointments
from models.clients import Clients
from models.appointments import AppointmentStatus
from models.availability import Availability
from models.reviews import Reviews
from utils.auth import hash_password, verify_password, create_access_token
from utils.cloudinary_utils import upload_image
import shutil
import tempfile
import os


counsellors_router=APIRouter(
    prefix="/counsellors",
    tags=["Counsellors"]
)

@counsellors_router.post("/upload-profile-image/{counsellor_id}")
async def upload_profile_image(counsellor_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    counsellor = db.query(Counsellors).filter(Counsellors.counsellors_id == counsellor_id).first()
    if not counsellor:
        raise HTTPException(status_code=404, detail="Counsellor not found")
    
    try:
        # Create a temporary file to store the upload
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
        
        # Upload to Cloudinary
        image_url = upload_image(tmp_path)
        
        # Remove temporary file
        os.remove(tmp_path)
        
        if not image_url:
            raise HTTPException(status_code=500, detail="Failed to upload image to Cloudinary")
        
        # Update counsellor database
        counsellor.profile_image = image_url
        db.commit()
        db.refresh(counsellor)
        
        return {"image_url": image_url, "message": "Profile image updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@counsellors_router.post("/signup", response_model=TokenResponse)
def signup(counsellors: Signup, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_counsellor = db.query(Counsellors).filter(Counsellors.email == counsellors.email).first()
    if existing_counsellor:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_counsellor = Counsellors(
        name=counsellors.name,
        email=counsellors.email,
        password=hash_password(counsellors.password),  # Hash the password
        role="counsellor",
        age=counsellors.age,
        gender=counsellors.gender,
        phone_number=counsellors.phone_number,
        speaks=counsellors.speaks,
        experience=counsellors.experience,
        address=counsellors.address,
        specialization=getattr(counsellors, 'specialization', "Counselling Psychologist"),
        expertise=getattr(counsellors, 'expertise', []),
        mode=getattr(counsellors, 'mode', ["Online"]),
        profile_image=getattr(counsellors, 'profile_image', None),
        about=getattr(counsellors, 'about', None)
    )
    db.add(new_counsellor)
    db.commit()
    db.refresh(new_counsellor)
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(new_counsellor.counsellors_id), "role": "counsellor"}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": new_counsellor
    }

@counsellors_router.post("/login", response_model=TokenResponse)
def login(data: Login, db: Session = Depends(get_db)):
    counsellor = db.query(Counsellors).filter(
        Counsellors.email == data.email
    ).first()

    if not counsellor:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not verify_password(data.password, counsellor.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(counsellor.counsellors_id), "role": "counsellor"}
    )

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
        password=hash_password(counsellors.password),
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
     ).outerjoin(Reviews, Reviews.counsellors_id == Counsellors.counsellors_id)\
     .filter(or_(Counsellors.status.in_(["active", "pending"]), Counsellors.status == None))\
     .group_by(Counsellors.counsellors_id)\
     .all()

    counsellors_list = []
    for counsellor, reviews_count, rating in results:
        # Convert model to dict to inject calculated fields
        counsellor.reviews_count = reviews_count
        counsellor.rating = round(rating, 1)
        counsellors_list.append(counsellor)

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
    ).outerjoin(Reviews, Reviews.counsellors_id == Counsellors.counsellors_id)\
     .filter(or_(Counsellors.status.in_(["active", "pending"]), Counsellors.status == None))

    if name:
        query = query.filter(Counsellors.name.ilike(f"%{name}%"))
    if specialization:
        query = query.filter(Counsellors.specialization.ilike(f"%{specialization}%"))
    if mode:
        query = query.filter(Counsellors.mode.contains([mode]))

    results = query.group_by(Counsellors.counsellors_id).all()

    counsellors_list = []
    for counsellor, reviews_count, rating in results:
        counsellor.reviews_count = reviews_count
        counsellor.rating = round(rating, 1)
        counsellors_list.append(counsellor)

    return counsellors_list

@counsellors_router.get("/{counsellor_id}")
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
        update_data["password"] = hash_password(update_data["password"])
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
    try:
        results = (
            db.query(
                Appointments.appointment_id,
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
        return [
            {
                "appointment_id": res.appointment_id,
                "date": str(res.date),
                "time": res.time,
                "client_name": res.client_name,
                "mode": res.mode,
                "counsellor_response": res.counsellor_response
            }
            for res in results
        ]
    except Exception as e:
        print(f"ERROR in upcoming_sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@counsellors_router.get("/{counsellor_id}/requests")
def session_requests(counsellor_id: int, db: Session = Depends(get_db)):
    try:
        results = (
            db.query(
                Appointments.appointment_id,
                Appointments.date,
                Appointments.time,
                Clients.name.label("client_name"),
                Appointments.mode,
                Appointments.counsellor_response,
                Appointments.status
            )
            .join(Clients, Clients.clients_id == Appointments.clients_id)
            .filter(
                Appointments.counsellors_id == counsellor_id,
                Appointments.status == AppointmentStatus.pending.value
            )
            .all()
        )
        return [
            {
                "appointment_id": res.appointment_id,
                "date": str(res.date),
                "time": res.time,
                "client_name": res.client_name,
                "mode": res.mode,
                "counsellor_response": res.counsellor_response,
                "status": res.status
            }
            for res in results
        ]

    except Exception as e:
        print(f"ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@counsellors_router.get("/{counsellor_id}/completed-sessions")
def completed_sessions(counsellor_id: int, db: Session = Depends(get_db)):
    try:
        results = (
            db.query(
                Appointments.appointment_id,
                Appointments.date,
                Appointments.time,
                Clients.name.label("client_name"),
                Appointments.mode,
                Appointments.status
            )
            .join(Clients, Clients.clients_id == Appointments.clients_id)
            .filter(
                Appointments.counsellors_id == counsellor_id,
                Appointments.status == AppointmentStatus.completed.value
            )
            .all()
        )
        return [
            {
                "appointment_id": res.appointment_id,
                "date": str(res.date),
                "time": res.time,
                "client_name": res.client_name,
                "mode": res.mode,
                "status": res.status
            }
            for res in results
        ]
    except Exception as e:
        print(f"ERROR in completed_sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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

    review_stats = db.query(
        func.count(Reviews.review_id).label("reviews_count"),
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