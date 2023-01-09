from pydantic import BaseModel,EmailStr,Field

class User(BaseModel):
    first_name:str
    last_name:str
    image:str
    password:str
    email:EmailStr

class CreateUser(BaseModel):
    first_name:str
    last_name:str
    password:str
    email:EmailStr

class AuthDetails(BaseModel):
    access_token:str
    refresh_token:str
    user:CreateUser

class Review(BaseModel):
    review:str
    rating:int = Field(..., gt=0, le=10)

class Login(BaseModel):
    email:EmailStr
    password:str
