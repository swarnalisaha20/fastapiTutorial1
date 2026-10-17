from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
import models
import schemas
from google import genai
import os
from google.genai import types
from dotenv import load_dotenv
load_dotenv()


router = APIRouter(
    prefix = "/notes",
    tags = ["Notes Apis"]
)


# AI Connection
ai_client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


#Learning Embedding
@router.post("/ai/embed")
async def create_embadding(request: schemas.SmartNoteCreate):

    #ask google to turn our text into numbers
    respose = ai_client.models.embed_content(
        model='gemini-embedding-001',
        contents=request.content
    )

    #grav the list of numbers
    vector = respose.embeddings[0].values

    return {
        "text": request.content,
        "total_numbers": len(vector),
        #just show the first 5
        "first_5_numbers": vector[:5]
    }


@router.post("/ai/classify-ticket")
async def classify_ticket(request: schemas.SmartNoteCreate):
    #We prepare "Few-shot" examples (showing the AI how to think)
    few_shot_prompt=f"""
You are a senior tech support triage agent. Classify ticktes bases on these examples:

Example 1:
Input: "Where can I download my last months's invoice PDF?"
Output: Urgency=LOW,Department=BILLING, Reason=Normal invoice download request.
Example 2:
Input: "Production database connection refused! All customers are seeing error 500!"
Output: Urgency=CRITICAL, Department=DATABASE, Reason=Production database outage affecting users.
Example 3:
Input: "The submit button has a small typo on the signup page."
Output: Urgency=LOW, Department=BACKEND, Reason=Minor UI typo with no business disruption.

now classify this new customer ticket:
Input: "{request.content}"
"""

    #Force it into our clean Pydantic schema
    ai_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=schemas.TicketClassification
    )

    response = ai_client.models.generate_content(
        model='gemini-3.8-flash',
        contents=few_shot_prompt,
        config=ai_config
    )

    return {"Ticket": response.text}


@router.post("/ai/analyze")
async def analyze_note(request: schemas.SmartNoteCreate):
    #defining -to return response as json
    #forcing Gemini to use Pydantic schema as JSON
    ai_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=schemas.NoteAnalysis
    )

    response = ai_client.models.generate_content(
        model='gemini-3.8-flash',
        contents=f"Analyze this text and extract information: {request.content}",
        config=ai_config
    )

    # e.g
    # "content": "I had a terrible day today. My Python code kept throwing 500 errors and my server crashed twice at work."

    # Response body
    # Download
    # {
    # "Analysis": "{\"summery\":\"The user experienced a frustrating day at work due to Python 500 errors and multiple server crashes.\",\"sentiment\":\"Negative\",\"category\":\"Software Development\",\"keyword\":[\"Python\",\"500 errors\",\"server crashed\",\"work\",\"errors\"]}"
    # }


    # response.text is guaranteed to be a valid JSON string!
    return {"Analysis": response.text}

# The AI Route - take simple response from AI
@router.post("/ai/chat")
async def chat_with_ai(request: schemas.PromptRequest):

    #create a secret system instruction
    ai_config = types.GenerateContentConfig(
        system_instruction="You are a grumpy old pirate. You always complain about tge modern internet before answering questions. Use pirate word like 'Arrr' and 'matey'."
    )
    # Send the user's message to the Gemini AI & the the Sectet configaration
    response = ai_client.models.generate_content(
        model = 'gemini-3.8-flash',
        contents=request.message,
        config=ai_config
    )

    # Return the AI's answer back to the user
    return {
        "ai_answer": response.text
    }
# async def chat_with_ai(request: schemas.PromptRequest):

#     # Send the user's message to the Gemini AI
#     response = ai_client.models.generate_content(
#         model = 'gemini-3.8-flash',
#         contents=request.message
#     )

#     # Return the AI's answer back to the user
#     return {
#         "ai_answer": response.text
#     }


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


@router.post("/notes/")
async def create_note(note : schemas.NoteCreate, db: AsyncSession = Depends(get_db)):
    embed_response = ai_client.models.embed_content(
        model='gemini-embedding-001',
        contents=note.content
    )

    vector = embed_response.embeddings[0].values
    

    #first simple version 
    # without storing embedding, next just added code to store pgembedding
    #here note = NoteCreate like setting how json data should be in request body
    new_note = models.Note(
        title=note.title, 
        content=note.content,
        #-------->our new pgvector column
        embedding=vector
        )

    #e.g.-add to shoping card & save to database(Commit)
    db.add(new_note)
    await db.commit()  #like $note->save() but for await code pauses after commit wait for response
    #to use await, we need to use keyword "async" 
    #Note: only this user's code is waiting. The rest of your web server is still awake and helping other users!

    await db.refresh(new_note)
    return {
        "message": "Note created successfully with AI Vector Embedding!",
        # "note": new_note,
        "id": new_note.id,
        "title": new_note.title,
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