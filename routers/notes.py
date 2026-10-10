from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
import models
import schemas
from google import genai
import os
from dotenv import load_dotenv
load_dotenv()


router = APIRouter(
    prefix = "/notes",
    tags = ["Notes Apis"]
)


# AI Connection
ai_client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


#*****as now we are useing router so rep
@router.post("/smart-notes")
# @app.post("/smart-notes")
async def create_smart_note(request: schemas.SmartNoteCreate, db: AsyncSession = Depends(get_db)):
    prompt = f"Please read this note and generate a short, 3-word title for it. Here is the note {request.content}"    
    ai_response = ai_client.models.generate_content(
        model='gemini-3.8-flash',
        contents = prompt,
    )

    generated_title = ai_response.text.strip()

    new_note = models.Note(title=generated_title, content=request.content)
    db.add(new_note)

    await db.commit()
    await db.refresh(new_note)

    return {
        "message": "Note craeted successfully",
        "note": new_note 
    }


# The AI Route - take simple response from AI
@router.post("/ai/chat")
async def chat_with_ai(request: schemas.PromptRequest):

    # Send the user's message to the Gemini AI
    response = ai_client.models.generate_content(
        model = 'gemini-3.8-flash',
        contents=request.message
    )

    # Return the AI's answer back to the user
    return {
        "ai_answer": response.text
    }


@router.post("/notes/")
async def create_note(note : schemas.NoteCreate, db: AsyncSession = Depends(get_db)):
    #here note = NoteCreate like setting how json data should be in request body
    new_note = models.Note(title=note.title, content=note.content)

    #e.g.-add to shoping card & save to database(Commit)
    db.add(new_note)
    await db.commit()  #like $note->save() but for await code pauses after commit wait for response
    #to use await, we need to use keyword "async" 
    #Note: only this user's code is waiting. The rest of your web server is still awake and helping other users!

    await db.refresh(new_note)
    return {
        "message": "Note created successfully!",
        "note": new_note
    }


@router.get("/notes/")
async def get_notes(db: AsyncSession = Depends(get_db)):
    #like Select * from notes
    query = select(models.Note)

    # Execute the query
    result = await db.execute(query)

    #Grab all the results and turn them into a normal list
    notes = result.scalars().all() #scalars helps to redesign data structure
    return {"notes": notes}


@router.get("/notes/{note_id}")
async def get_single_note(note_id:int, db:AsyncSession = Depends(get_db)):
    query = select(models.Note).where(models.Note.id==note_id)
    result = await db.execute(query) #Execute the query

    #Strip the wrapper using scalar and grab just the FIRST note it finds
    note = result.scalar_one_or_none()

    if note is None:
        return {"error": "No data found"}

    return {"note": note}


@router.put("/notes/{note_id}")
async def update_note(note_id: int, update_data:schemas.NoteCreate, db:AsyncSession=Depends(get_db)):
    query = select(models.Note).where(models.Note.id == note_id)
    result =  await db.execute(query)
    note = result.scalar_one_or_none()

    if note is None:
        return {"error": "No data found"}

    #Change the data 
    # (We are borrowing our NoteCreate class to validate the new incoming JSON)
    note.title = update_data.title
    note.content = update_data.content

    # Save the changes to the database
    await db.commit()
    await db.refresh(note)

    return {"message": "Note updated successfully!",
            "note": note}


@router.delete("/notes/{note_id}")
async def delete_note(note_id:int, db:AsyncSession=Depends(get_db)):
    query = select(models.Note).where(models.Note.id == note_id)
    result = await db.execute(query)
    note = result.scalar_one_or_none()

    if note is None:
        return {"error": "No data found"}

    #Tell the shopping cart to delete it
    await db.delete(note)
    # Save the changes to the database
    await db.commit()

    return {"message": "Note deleted successfully!"}