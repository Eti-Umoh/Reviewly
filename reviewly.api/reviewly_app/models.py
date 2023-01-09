from sqlalchemy import Column,Integer,String,ForeignKey,TEXT,DateTime
from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    image = Column(String(255))
    password = Column(String(255))
    email = Column(String(255), unique=True)
    review = relationship('Review',back_populates='writer')

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    review = Column(TEXT)
    rating = Column(Integer)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    writer = relationship('User', back_populates='review')