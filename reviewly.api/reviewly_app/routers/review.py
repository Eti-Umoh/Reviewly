from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from ..utils import get_current_user,get_image_url,get_video_url,get_review_by_id
from .. import crud,schemas,models
from ..database import get_db
from fastapi.responses import Response
from sqlalchemy.orm import Session 
from PIL import Image
from typing import List


router = APIRouter(tags=['Review'],prefix='/review')
review_crud = crud.ReviewCrud
user_helpful_crud = crud.UserHelpfulCrud


@router.post('/post_review')
def post_review(response:Response,payload:schemas.CreateReview,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401,detail='Please log in')
    Review = review_crud.create_review(db,payload)
    Review.user_id=user.id
    db.commit()
    db.refresh(Review)
    return {'review':Review}

@router.post('/review_image')
async def add_image_to_review(id,image: UploadFile = File(...),user:dict=Depends(get_current_user),db:Session = Depends(get_db)):
    if not user:
        raise  HTTPException(status_code=404, detail="User not found")
    current_review = get_review_by_id(db,id)
    if user.id == current_review.user_id:
        image_url = await get_image_url(image)
        current_review.image=image_url
        db.commit()
        db.refresh(current_review)
    else:
        raise  HTTPException(status_code=404, detail="Review does not belong to this user")
    return {'image':image_url}


@router.post('/review_video')
async def add_video_to_review(id,video: UploadFile = File(...),user:dict=Depends(get_current_user),db:Session = Depends(get_db)):
    if not user:
        raise  HTTPException(status_code=404, detail="User not found")
    current_review = get_review_by_id(db,id)
    if user.id == current_review.user_id:
        video_url = await get_video_url(video)
        current_review.video=video_url
        db.commit()
        db.refresh(current_review)
    else:
        raise  HTTPException(status_code=404, detail="Review does not belong to this user")
    return {'video':video_url}

@router.post('/helpful')
def mark_review_as_helpful(id,user:dict=Depends(get_current_user),db:Session = Depends(get_db)):
    if not user:
        raise  HTTPException(status_code=404, detail="User not found")
    current_review = get_review_by_id(db,id)
    check_review_id_and_user_id = db.query(models.UserHelpful).filter(models.UserHelpful.review_id==current_review.id,models.UserHelpful.user_id==user.id).first()
    if check_review_id_and_user_id:
            mark = current_review.helpful-1
            current_review.helpful = mark
            db.query(models.UserHelpful).filter(models.UserHelpful.review_id==current_review.id,models.UserHelpful.user_id==user.id).delete(synchronize_session=False)
            db.commit()
            db.refresh(current_review)
    else:
        mark = current_review.helpful+1
        current_review.helpful = mark
        db.commit()
        db.refresh(current_review)
        user_helpful = user_helpful_crud.create_user_helpful(db,user.id,current_review.id)
    return {'Successful'}

@router.get('/all_reviews',response_model=List[schemas.Review])
def all_reviews(user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401,detail='Please log in')
    all_reviews = review_crud.get_all_reviews(db)
    return all_reviews

@router.get('/most_helpful_reviews',response_model=List[schemas.Review])
def most_helpful_reviews(user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401,detail='Please log in')
    all_reviews = review_crud.get_most_helpful_reviews(db)
    return all_reviews