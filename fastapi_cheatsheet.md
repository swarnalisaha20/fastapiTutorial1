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
*Go to `http://127.0.0.1:8000/docs` to see the auto-generated testing UI (Swagger).*

### 3. Basic Routing (Like Laravel Routes)
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}
```

### 4. Data Validation with Pydantic (Like Laravel Form Requests)
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
def create_item(item: Item):
    return {"message": f"Item {item.name} costs {item.price}"}
```

### 5. Database Setup (SQLAlchemy)
In Laravel you use `Eloquent` and `.env`. In FastAPI, we create `database.py`:
```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Connect to Postgres
DATABASE_URL = "postgresql+asyncpg://postgres:root@localhost/fastapi_ai"
engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(bind=engine)
Base = declarative_base()
```

### 6. Database Models (Like Laravel Model + Migration)
In `models.py`:
```python
from sqlalchemy import Column, Integer, String, Text
from database import Base

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    content = Column(Text)
```

### 7. Auto-Create Tables on Startup
In `main.py`, use a `lifespan` event to create tables automatically (like `php artisan migrate`):
```python
from contextlib import asynccontextmanager
from database import engine
import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)
```
