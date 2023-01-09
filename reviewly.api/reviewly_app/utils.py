from passlib.context import CryptContext
from . import models
from sqlalchemy.orm import Session
from fastapi import HTTPException


SECRET_KEY='secret'
ALGORITHM='HS256'
ACCESS_TOKEN_LIFETIME_MINUTES= 43200
REFRESH_TOKEN_LIFETIME=14
access_cookies_time=ACCESS_TOKEN_LIFETIME_MINUTES * 60
refresh_cookies_time=REFRESH_TOKEN_LIFETIME*3600*24

pwd_hash=CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password):
    return pwd_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_hash.verify(plain_password, hashed_password)

def get_user_by_id(db,id:str):
        return db.query(models.User).filter(models.User.id==id).first()

def get_user_by_email(db,email:str):
        return db.query(models.User).filter(models.User.email==email).first()

def authenticate(db:Session,email:str, password:str):
    user=get_user_by_email(db, email)
    exception= HTTPException(status_code=400, detail='invalid email or password')
    if not user:
        raise exception
    if not verify_password(password, user.password):
        raise exception
    return user

