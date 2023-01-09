from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from .. import schemas,crud
from ..database import get_db
from ..utils import get_user_by_email
from fastapi.responses import Response
from sqlalchemy.orm import Session
from ..utils import  authenticate, REFRESH_TOKEN_LIFETIME, ACCESS_TOKEN_LIFETIME_MINUTES, access_cookies_time, refresh_cookies_time
from datetime import timedelta

router = APIRouter(tags=['Authentication'],prefix='/auth')
authjwt_secret_key = "random"

@router.post('/signup', response_model=schemas.AuthDetails, status_code=201)
def signup(response:Response,payload:schemas.CreateUser, Authorize:AuthJWT=Depends(),db:Session=Depends(get_db)):
    user_crud=crud.UserCrud
    if get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail='user with this email already exists')
    User=user_crud.create_user(db, payload)
    access_token=Authorize.create_access_token(subject=User.id, expires_time=timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES))
    refresh_token=Authorize.create_refresh_token(subject=User.id, expires_time=timedelta(days=REFRESH_TOKEN_LIFETIME))
    response.set_cookie(key='access_token',value=access_token, expires=access_cookies_time, max_age=access_cookies_time, httponly=True)
    response.set_cookie(key='refresh_token',value=refresh_token, expires=refresh_cookies_time, max_age=refresh_cookies_time, httponly=True)
    return {'access_token':access_token, 'refresh_token':refresh_token, 'user':User}


@router.post('/login', status_code=200, response_model=schemas.AuthDetails)
def login( response:Response,payload:schemas.Login,Authorize:AuthJWT=Depends() ,db:Session=Depends(get_db)):
    password, email=payload.password, payload.email
    user=authenticate(db=db, password=password, email=email)
    access_token=Authorize.create_access_token(subject=user.id, expires_time=timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES))
    refresh_token=Authorize.create_refresh_token(subject=user.id, expires_time=timedelta(days=REFRESH_TOKEN_LIFETIME))
    response.set_cookie(key='access_token',value=access_token, expires=access_cookies_time, max_age=access_cookies_time, httponly=True)
    response.set_cookie(key='refresh_token',value=refresh_token, expires=refresh_cookies_time, max_age=refresh_cookies_time, httponly=True)
    return {'access_token':access_token, 'refresh_token':refresh_token, 'user':user}

@router.post('/logout')
def logout(Authorize:AuthJWT=Depends()):
    Authorize.unset_jwt_cookies()

    return {'message':'successfully logged out'}