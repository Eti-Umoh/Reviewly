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
    password:str=Field(min_length=6, description='password minimum length is 8 characters')
    email:EmailStr
    class Config:
        orm_mode=True

class SignUpDetails(BaseModel):
    user:CreateUser

class AuthDetails(BaseModel):
    access_token:str
    refresh_token:str
    user:CreateUser

class Login(BaseModel):
    email:EmailStr
    password:str

class Review(BaseModel):
    review:str
    rating:int = Field(..., gt=0, le=10, description='maximum value for rating is 10')
    image:str
    video:str
    helpful:str

class CreateReview(BaseModel):
    review:str
    rating:int = Field(..., gt=0, le=10, description='maximum value for rating is 10')

class ImageUpdate(BaseModel):
    image:str