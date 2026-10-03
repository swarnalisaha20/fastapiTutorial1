from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from database import engine,get_db
from pydantic import BaseModel
import models
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


# Note:
# In Laravel, if you want something to happen when your application boots up, 
# you might put it in the boot() method of a Service Provider. In FastAPI, we use this lifespan function for that exact same purpose.

# 1. This function runs right before the server starts
#asynccontextmanager - This is a special Python tag. It tells FastAPI: 
# "Hey, this function handles the entire life of the app (from the moment it starts, to the moment it stops)."
@asynccontextmanager 
async def lifespan(app: FastAPI):
    print("Server is starting... creating tables!")
    # This is the magic command that creates your database tables:
    async with engine.begin() as conn:
        #makes connectiom
        await conn.run_sync(models.Base.metadata.create_all) #models.Base.metadata holds list of models, create_all makes table if doesn't exist
    print("Tables created successfully!")
    yield 
    # This tells FastAPI to continue starting the server 
    #yield This is a special Python keyword. It essentially means:
    #  "Okay, we finished the setup. Pause this function right here and
    #  let the web server start running for the users!" (Fun fact: If you ever press Ctrl+C to kill your server, FastAPI will come right back to this yield line and run any code you put below it to clean things up).



# 2. Add the lifespan to your app
app = FastAPI(lifespan=lifespan)
# app = FastAPI()


# Tutorial 2 - CRUD
#BaseModel is the Pydentic Model for form validation
#(Like a Laravel Form Request to check data)
class NoteCreate(BaseModel):
    title: str
    content: str


@app.post("/notes/")
async def create_note(note : NoteCreate, db: AsyncSession = Depends(get_db)):
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


@app.get("/notes/")
async def get_notes(db: AsyncSession = Depends(get_db)):
    #like Select * from notes
    query = select(models.Note)

    # Execute the query
    result = await db.execute(query)

    #Grab all the results and turn them into a normal list
    notes = result.scalars().all() #scalars helps to redesign data structure
    return {"notes": notes}


@app.get("/notes/{note_id}")
async def get_single_note(note_id:int, db:AsyncSession = Depends(get_db)):
    query = select(models.Note).where(models.Note.id==note_id)
    result = await db.execute(query) #Execute the query

    #Strip the wrapper using scalar and grab just the FIRST note it finds
    note = result.scalar_one_or_none()

    if note is None:
        return {"error": "No data found"}

    return {"note": note}


@app.put("/notes/{note_id}")
async def update_note(note_id: int, update_data:NoteCreate, db:AsyncSession=Depends(get_db)):
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


@app.delete("/notes/{note_id}")
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

# Tutorial 1
# app = FastAPI()


# # 1. Create a Pydantic Model (This acts like a Laravel Form Request)
# class Item(BaseModel):
#     name:str
#     price:float
#     description:str | None=None # This means 'description' is optional


# #Eg. of route define
# @app.get("/")
# def home():
#     return {"message": "Hello World"}


# # 2. Create a POST route to receive data
# @app.post("/items/")
# def create_item(item: Item):
#     # FastAPI automatically checks if 'name' is a string and 'price' is a float!
#     # If the user sends a string for price (like "ten"), FastAPI automatically throws a 422 Error
#     return {
#         "success": True,
#         "message": f"Item {item.name} created",
#         "price": item.price
#     }