from fastapi import Depends
from . import models,schemas
from .utils import hash_password


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
    
class UserHelpfulCrud:
    def create_user_helpful(db,user_id,review_id):
        user_helpful = models.UserHelpful(user_id=user_id,review_id=review_id)
        db.add(user_helpful)  
        db.commit()
        db.refresh(user_helpful)
        return user_helpful  
