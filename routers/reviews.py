from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from dependencies import get_db
from models.reviews import Reviews
from schemas.reviews import ReviewCreate, ReviewResponse , ReviewUpdate

reviews_router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)

@reviews_router.post("/create", response_model=ReviewResponse)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    new_review = Reviews(
        clients_id=review.clients_id,
        counsellors_id=review.counsellors_id,
        rating=review.rating,
        comments=review.comments
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@reviews_router.get("/all", response_model=List[ReviewResponse])
def get_all_reviews(db: Session = Depends(get_db)):
    return db.query(Reviews).filter(Reviews.is_active == True).all()

@reviews_router.get("/counsellor/{counsellors_id}", response_model=List[ReviewResponse])
def get_reviews_for_counsellor(counsellors_id: int, db: Session = Depends(get_db)):
    return db.query(Reviews)\
        .filter(
            Reviews.counsellors_id == counsellors_id,
            Reviews.is_active == True
        ).all()

@reviews_router.put("/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int, review: ReviewUpdate, db: Session = Depends(get_db)):
    db_review = db.query(Reviews)\
        .filter(Reviews.review_id == review_id, Reviews.is_active == True)\
        .first()

    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    if review.rating is not None:
        db_review.rating = review.rating
    if review.comments is not None:
        db_review.comments = review.comments

    db.commit()
    db.refresh(db_review)
    return db_review

@reviews_router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Reviews)\
        .filter(Reviews.review_id == review_id, Reviews.is_active == True)\
        .first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    review.is_active = False
    db.commit()
    return {"message": "Review deleted successfully"}

@reviews_router.get("/counsellor/{counsellors_id}/average-rating")
def average_rating(counsellors_id: int, db: Session = Depends(get_db)):
    avg = db.query(func.avg(Reviews.rating))\
            .filter(
                Reviews.counsellors_id == counsellors_id,
                Reviews.is_active == True
            ).scalar()

    return {
        "counsellors_id": counsellors_id,
        "average_rating": round(avg, 2) if avg else 0
    }

@reviews_router.get("/counsellor/{counsellors_id}/count")
def review_count(counsellors_id: int, db: Session = Depends(get_db)):
    count = db.query(Reviews)\
        .filter(
            Reviews.counsellors_id == counsellors_id,
            Reviews.is_active == True
        ).count()

    return {
        "counsellors_id": counsellors_id,
        "total_reviews": count
    }
