# FastAPI Cheat Sheet (Day 1)

### 1. Project Setup
```powershell
python -m venv venv           # Create virtual environment
.\venv\Scripts\activate       # Activate it (Windows)
pip install "fastapi[all]"    # Install FastAPI
pip install "sqlalchemy[asyncio]" asyncpg  # Install Database tools
```

### 2. Run the Server
```powershell
uvicorn main:app --reload
```
*Note: `--reload` restarts the server automatically when you save. Go to `http://127.0.0.1:8000/docs` to see the auto-generated testing UI (Swagger).*

### 3. Basic Routing (Like Laravel Routes)
```python
from fastapi import FastAPI

app = FastAPI()

# @app.get("/") is a decorator. It tells FastAPI this function handles GET requests to the home page (like Route::get in Laravel)
@app.get("/")
def home():
    return {"message": "Hello World"}
```

### 4. Data Validation with Pydantic (Like Laravel Form Requests)
```python
from pydantic import BaseModel

# BaseModel automatically validates data (e.g. makes sure price is a number). 
# If a user sends bad data, FastAPI automatically returns a 422 Error.
class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
def create_item(item: Item):
    return {"message": f"Item {item.name} costs {item.price}"}
```

### 5. Database Setup (SQLAlchemy) in `database.py`
In Laravel you use `Eloquent` and `.env`. In FastAPI, we write a file to connect:
```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# 1. Connection String: Like your .env file
DATABASE_URL = "postgresql+asyncpg://postgres:root@localhost/fastapi_ai"

# 2. Engine: The actual machine that physically talks to Postgres. It manages the connection.
engine = create_async_engine(DATABASE_URL)

# 3. SessionLocal: A temporary workspace (like a shopping cart). 
# You put data here, and when you are ready, you "commit" it to save it.
SessionLocal = async_sessionmaker(bind=engine)

# 4. Base: The master class. Every model we make will inherit this (like 'extends Model' in Laravel)
Base = declarative_base()
```

### 6. Database Models in `models.py`
Combines Laravel's Model and Migration into one file:
```python
from sqlalchemy import Column, Integer, String, Text
from database import Base

class Note(Base):
    __tablename__ = "notes"
    
    # index=True is like an index in a book. It tells Postgres to make searching by this column instantly fast!
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    content = Column(Text)
```

### 7. Auto-Create Tables on Startup (in `main.py`)
This replaces `php artisan migrate`. It automatically creates tables when the server starts.
```python
from contextlib import asynccontextmanager
from database import engine
import models

# @asynccontextmanager tells FastAPI this function manages the "startup" and "shutdown" life of the app
@asynccontextmanager
async def lifespan(app: FastAPI):
    # engine.begin() safely opens the door to the database
    async with engine.begin() as conn:
        # models.Base.metadata holds a list of all your models. 
        # create_all tells Postgres to physically build the tables if they don't exist.
        await conn.run_sync(models.Base.metadata.create_all)
    
    # yield means "pause here and let the server run for users"
    yield

app = FastAPI(lifespan=lifespan)
```

### 8. Managing Database Connections Safely (`get_db`)
Because FastAPI runs constantly, we must safely open and close the database connection for every single user request so the server doesn't crash from memory overload.
```python
async def get_db():
    # 1. Open a new temporary session (shopping cart) for the user
    db = SessionLocal()  
    try:
        # 2. Hand the session over to the route to do its job
        yield db         
    finally:
        # 3. No matter what happens (even errors), ALWAYS safely close the connection!
        await db.close() 
```

### 9. Using the Database in a Route (`Depends`)
To actually use our database inside a route, we use **Dependency Injection**. 
```python
from fastapi import Depends

# Depends(get_db) tells FastAPI: "Before running this route, run get_db() first, give me the 'db' session, and close it when I'm done!"
@app.get("/notes")
def get_all_notes(db = Depends(get_db)):
    return {"message": "This route now has safe access to the database!"}
```

### 10. Async, Await, and Saving Data (Quick Answers)

* **Why use `async def`?**
  If you want to use the word `await` inside a function, Python forces you to start the function with `async def`.

* **What does `await` do?**
  It means "pause right here". When you say `await db.commit()`, the code pauses until the database finishes saving. While it waits, the server goes to help other users (it never freezes!).

* **Why `db.add()` and then `db.commit()`?**
  SQLAlchemy works like a shopping cart:
  1. `db.add()`: Puts data in your cart (not saved to database yet).
  2. `db.commit()`: Clicks "Checkout" (physically saves to the database).
  This is great because you can add 10 items to your cart, and save them all at the exact same time with just one `commit()`!

### 11. Reading Data (GET)
To read data in SQLAlchemy, we have to build a query, execute it, and strip the wrapper.
```python
from sqlalchemy import select

# GET ALL NOTES
@app.get("/notes/")
async def get_notes(db: AsyncSession = Depends(get_db)):
    query = select(models.Note)
    result = await db.execute(query)
    # .scalars().all() strips away the weird grid wrapper and gives a clean list
    notes = result.scalars().all() 
    return {"notes": notes}

# GET ONE NOTE BY ID
@app.get("/notes/{note_id}")
async def get_single_note(note_id: int, db: AsyncSession = Depends(get_db)):
    query = select(models.Note).where(models.Note.id == note_id)
    result = await db.execute(query)
    # .scalar_one_or_none() grabs exactly one note, or returns None if missing
    note = result.scalar_one_or_none()
    return {"note": note}
```

### 12. Updating Data (PUT)
Find it, change it, and commit it!
```python
@app.put("/notes/{note_id}")
async def update_note(note_id: int, update_data: NoteCreate, db: AsyncSession = Depends(get_db)):
    # ... find the note first ...
    note.title = update_data.title
    note.content = update_data.content
    await db.commit()
    await db.refresh(note)
    return {"note": note}
```

### 13. Deleting Data (DELETE)
Find it, delete it, and commit it!
```python
@app.delete("/notes/{note_id}")
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db)):
    # ... find the note first ...
    await db.delete(note)
    await db.commit()
    return {"message": "Deleted!"}
```

### 14. Quick Debugging & Questions (Day 2)

* **Why did my Swagger UI JSON box disappear?**
  If you write `note = NoteCreate`, Python thinks you are setting a default value, which ruins the Swagger interface. Always use a colon for Type Hints: `note: NoteCreate`.

* **What does `await db.refresh(new_note)` do?**
  When you save a new note to PostgreSQL, the database automatically creates an `id` for it. `db.refresh()` tells Python to quickly look at the database and grab that new `id` so your code can use it immediately in the API response.
