from fastapi import APIRouter, Depends, HTTPException
from ..utils import get_current_user
from .. import crud,schemas
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
    Review.user_id = user.id
    return {'review':Review}
