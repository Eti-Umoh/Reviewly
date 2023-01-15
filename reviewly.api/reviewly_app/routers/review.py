from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from ..utils import get_current_user,get_image_url
from .. import crud,schemas,models
from ..database import get_db
from fastapi.responses import Response
from sqlalchemy.orm import Session 
from PIL import Image


router = APIRouter(tags=['Review'],prefix='/review')
review_crud = crud.ReviewCrud

@router.post('/post_review')
def post_review(response:Response,payload:schemas.CreateReview,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401,detail='Please log in')
    Review = review_crud.create_review(db,payload)
    Review.user_id=user.id
    db.commit()
    db.refresh(Review)
    return {'review':Review}

@router.post('review_image')
async def add_image_to_review(id,image: UploadFile = File(...),user:dict=Depends(get_current_user),db:Session = Depends(get_db)):
    if not user:
        raise  HTTPException(status_code=404, detail="User not found")
    current_review = db.query(models.Review).filter(models.Review.id == id).first()
    if user.id == current_review.user_id:
        image_url = await get_image_url(image)
        current_review.image=image_url
        db.commit()
        db.refresh(current_review)
    else:
        raise  HTTPException(status_code=404, detail="Review does not belong to this user")
    return {'image':image_url}
