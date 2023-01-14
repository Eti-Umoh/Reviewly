from fastapi import HTTPException, Depends, Cookie, Header, File, UploadFile
from fastapi_jwt_auth import AuthJWT
from passlib.context import CryptContext
from . import models
from sqlalchemy.orm import Session
from .database import get_db
from dotenv import load_dotenv
from PIL import Image
import secrets
import os
load_dotenv()


SECRET_KEY= os.getenv('SECRET_KEY')
authjwt_secret_key = os.getenv('authjwt_secret_key')
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

def get_current_user(Authorize:AuthJWT=Depends(), db:Session=Depends(get_db), access_token:str=Cookie(default=None),Bearer=Header(default=None)):
    exception=HTTPException(status_code=401, detail='invalid access token or access token has expired', headers={'WWW-Authenticate': 'Bearer'})

    try:

        Authorize.jwt_required()
        user_id=Authorize.get_jwt_subject()
        user=get_user_by_id(db, user_id)
        return user
    except:
        raise exception

async def get_image_url(file: UploadFile = File(...)):
    FILEPATH = "./static/"
    filename = file.filename
    extension= filename.split(".")[1]
    if extension not in ['png', 'jpg']:
        return {'status': "error", 'detail':"Image type not allowed"}
    token_name= secrets.token_hex(8)+"."+extension
    generated_name=FILEPATH + token_name
    file_content= await file.read()

    with open(generated_name, 'wb') as file:
        file.write(file_content)

    img = Image.open(generated_name)
    resized_image = img.resize(size=(200, 200))
    resized_image.save(generated_name)
    
    file.close()
    file_url = generated_name[1:]
    return file_url