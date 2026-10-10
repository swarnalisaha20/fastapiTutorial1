from pydantic import BaseModel


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
