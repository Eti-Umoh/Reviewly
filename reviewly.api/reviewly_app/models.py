from sqlalchemy import Column,Integer,String,ForeignKey
from .database import Base
from sqlalchemy.orm import relationship 

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    image = Column(String(255))
    password = Column(String(255))
    email = Column(String(255), unique=True)