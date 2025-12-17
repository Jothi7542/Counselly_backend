from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from models.counsellors import Counsellors
from schemas.counsellors import CounsellorsCreate,CounsellorsUpdate,Signup,Login

counsellors_router=APIRouter(
    prefix="/consellors",
    tags=["counsellors"]
)

@counsellors_router.post("/signup")
def signup(counsellors: Signup, db: Session = Depends(get_db)):
    signup = Counsellors(
        name=counsellors.name,
        email=counsellors.email,
        password=counsellors.password,
        role=counsellors.role,
        age=counsellors.age,
        gender=counsellors.gender,
        phone_number=counsellors.phone_number,
        speaks=counsellors.speaks,
        specialization=counsellors.specialization,
        experience=counsellors.experience,
        expertise=counsellors.expertise,
        mode=counsellors.mode,
        about=counsellors.about,
        address=counsellors.address,
        profile_image=counsellors.profile_image
    )
    db.add(signup)
    db.commit()
    db.refresh(signup)
    return signup

@counsellors_router.post("/login")
def login(counsellors:Login, db:Session=Depends(get_db)):
    login=Counsellors(
        email=counsellors.email,
        password=counsellors.password
    )
    db.add(login)
    db.commit()
    db.refresh(login)
    return login

@counsellors_router.post("/create")
def add_counsellors(counsellors: CounsellorsCreate, db: Session = Depends(get_db)):
    new_counsellors = Counsellors(
        counsellors_id=counsellors.counsellors_id,
        name=counsellors.name,
        email=counsellors.email,
        password=counsellors.password,
        role=counsellors.role,
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
        availability=counsellors.availability,
        slot=counsellors.slot,
        status=counsellors.status,
        address=counsellors.address,
        created_at=counsellors.created_at
    )
    db.add(new_counsellors)
    db.commit()
    db.refresh(new_counsellors)
    return new_counsellors


@counsellors_router.get("/")
def all_counsellors(db:Session=Depends(get_db)):
    already_counsellors=db.query(Counsellors).all()
    db.close()
    return already_counsellors

@counsellors_router.get("/{counsellor_id}")
def counsellors_id(counsellor_id:int , db:Session=Depends(get_db)):
    already_counsellors=db.query(Counsellors).filter(Counsellors.counsellors_id==counsellor_id).first()
    db.close()
    return already_counsellors


@counsellors_router.put("/updateCounsellors/{counsellors_id}")
def update_counsellors(counsellor_id:int , counsellors:CounsellorsUpdate, db:Session=Depends(get_db)):
    update_counsellors=db.query(Counsellors).filter(Counsellors.counsellors_id == counsellor_id).first()
    if update_counsellors:
        update_counsellors.name=counsellors.name
        update_counsellors.email=counsellors.email
        update_counsellors.password=counsellors.password
        update_counsellors.age=counsellors.age
        update_counsellors.gender=counsellors.gender
        update_counsellors.phone_number=counsellors.phone_number
        update_counsellors.specialization=counsellors.specialization
        update_counsellors.address=counsellors.address
        update_counsellors.experience=counsellors.experience
        update_counsellors.expertise=counsellors.expertise
        update_counsellors.mode=counsellors.mode
        update_counsellors.about=counsellors.about
        update_counsellors.speaks=counsellors.speaks
        update_counsellors.profile_image=counsellors.profile_image
        update_counsellors.availability=counsellors.availability
        update_counsellors.slot=counsellors.slot
        db.commit()
        db.refresh(update_counsellors)
        db.close()
        return update_counsellors
    return {"message": "Counsellors not found"}


@counsellors_router.delete("/deleteCounsellors/{counsellors_id}")
def delete_counsellors(counsellors_id:int , db:Session=Depends(get_db)):
    delete_counsellors=db.query(Counsellors).filter(Counsellors.counsellors_id==counsellors_id).first()
    if delete_counsellors:
        db.delete(delete_counsellors)
        db.commit()
        return {"message": "Counsellors deleted successfully"}
    return {"message": "Counsellors not found"}

@counsellors_router.put("/updateCounsellors/{counsellors_id}")
def update_counsellors(counsellors_id: int, counsellors: CounsellorsUpdate, db: Session = Depends(get_db)):
    update_counsellor = db.query(Counsellors).filter(Counsellors.counsellors_id == counsellors_id ).first()

    if not update_counsellor:
        return {"message": "Counsellor not found"}

    update_counsellor.expertise = counsellors.expertise    

    db.commit()
    db.refresh(update_counsellor)
    return update_counsellor
