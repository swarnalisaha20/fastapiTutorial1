from sqlalchemy import Column, Integer, String, Text
from database import Base #to make model


# This file acts as BOTH your Model and your Migration! 
#we dont need to create migrations file here
class Note(Base):
    __tablename__= "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    content = Column(Text)