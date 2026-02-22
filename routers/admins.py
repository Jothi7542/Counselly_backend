from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models.admins import Admins
from schemas.admins import AdminCreate, AdminLogin, AdminTokenResponse
from auth_utils import get_password_hash, verify_password, create_access_token

admins_router = APIRouter(
    prefix="/admins",
    tags=["Admins"]
)

@admins_router.post("/signup", response_model=AdminTokenResponse)
def signup(data: AdminCreate, db: Session = Depends(get_db)):
    # Check if email exists
    existing = db.query(Admins).filter(Admins.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_admin = Admins(
        name=data.name,
        email=data.email,
        password=get_password_hash(data.password),
        role="admin"
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    access_token = create_access_token(data={"sub": new_admin.email, "role": "admin"})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": new_admin
    }

@admins_router.post("/login", response_model=AdminTokenResponse)
def login(data: AdminLogin, db: Session = Depends(get_db)):
    admin = db.query(Admins).filter(Admins.email == data.email).first()

    if not admin or not verify_password(data.password, admin.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": admin.email, "role": "admin"})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": admin
    }

from models.counsellors import Counsellors

@admins_router.get("/review-queue")
def get_review_queue(db: Session = Depends(get_db)):
    return db.query(Counsellors).order_by(Counsellors.created_at.desc()).all()
