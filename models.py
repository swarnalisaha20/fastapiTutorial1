from sqlalchemy import Column, Integer, String, Text
from database import Base #to make model
from pgvector.sqlalchemy import Vector


# This file acts as BOTH your Model and your Migration! 
#we dont need to create migrations file here
class Note(Base):
    __tablename__= "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    content = Column(Text)
    #after installing vector we added this column of type vector
    #for Gemini embedding!
    embedding = Column(Vector(3072), nullable=True)