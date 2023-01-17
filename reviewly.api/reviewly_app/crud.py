from fastapi import Depends
from . import models,schemas
from .utils import hash_password
from sqlalchemy import desc


class UserCrud:
    def create_user(db,payload:schemas.CreateUser):
        password=hash_password(payload.password)
        user=models.User(email=payload.email, password=password, first_name=payload.first_name, last_name=payload.last_name )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

class ReviewCrud:
    def create_review(db,payload:schemas.CreateReview):
        review =models.Review(review=payload.review,rating=payload.rating)
        db.add(review)
        db.commit()
        db.refresh(review)
        return review
    
    def get_all_reviews(db):
        all_reviews = db.query(models.Review).order_by(models.Review.date_created.desc()).all()
        return all_reviews

    def get_most_helpful_reviews(db):
        all_reviews = db.query(models.Review).order_by(models.Review.helpful.desc()).all()
        return all_reviews

    
class UserHelpfulCrud:
    def create_user_helpful(db,user_id,review_id):
        user_helpful = models.UserHelpful(user_id=user_id,review_id=review_id)
        db.add(user_helpful)  
        db.commit()
        db.refresh(user_helpful)
        return user_helpful  
