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
    user_helpful = relationship('UserHelpful', back_populates='creator')

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    review = Column(String(255))
    rating = Column(Integer)
    image = Column(String(255),nullable=True)
    video = Column(String(255),nullable=True)
    helpful = Column(Integer,default=0)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    writer = relationship('User', back_populates='review')
    user_helpful = relationship('UserHelpful', back_populates='review')

class UserHelpful(Base):
    __tablename__= "user_helpfuls"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    review_id = Column(Integer, ForeignKey('reviews.id'))
    creator = relationship('User', back_populates='user_helpful')
    review = relationship('Review',back_populates='user_helpful')