from pydantic import BaseModel
from typing import List


#BaseModel is the Pydentic Model for form validation
#(Like a Laravel Form Request to check data)
class NoteCreate(BaseModel):
    title: str
    content: str


class SmartNoteCreate(BaseModel):
    content: str


#Create a Pydantic Model to check the incoming user message like validator
class PromptRequest(BaseModel):
    message:str


#This is the exact json structure we will Force the AI to return
class NoteAnalysis(BaseModel):
    summery: str       # e.g. "positive", "negative", or "neutral"
    sentiment: str   
    category: str      #e.g. "Work", "Personal", "Study"
    keyword: List[str] # e.g. ["fastapi", "python", "backend"]


class TicketClassification(BaseModel):
    urgency: str
    department: str
    reason: str


class SearchQuery(BaseModel):
    question: str