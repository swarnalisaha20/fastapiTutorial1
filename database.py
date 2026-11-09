from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# 1. Your Database URL (Change "postgres:root" to your pgAdmin username and password!)
# Format: postgresql+asyncpg://user:password@localhost/database_name
# DATABASE_URL = "postgresql+asyncpg://postgres:root@localhost/fastapi_ai"
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/fastapi_ai"

# 2. Create the "Engine" (This does the actual communicating with Postgres)
engine = create_async_engine(DATABASE_URL, echo=True)

# 3. Create a Session (This is like a temporary workspace to run queries)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base Class (All our database models will inherit from this)
Base = declarative_base()

# 5. Dependency Function (We use this to give a database session to our routes)
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()