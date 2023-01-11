from fastapi import APIRouter, HTTPException, Depends
from ..utils import get_current_user


router = APIRouter(tags=['User'],prefix='/user')

@router.get('/profile')
def view_user(user:dict=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401,detail='user not found')
    return {
        'first_name':user.first_name,
        'last_name':user.last_name,
        'image':user.image,
        'email':user.email,
        'review':user.review
        }


