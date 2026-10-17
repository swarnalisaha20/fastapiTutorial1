# Master Learning Roadmap & Context for AI Assistant

***⚠️ IMPORTANT DIRECTIVE FOR AI ON ANY COMPUTER ⚠️***
**The user is a Laravel developer transitioning into a professional GenAI Developer using FastAPI + PostgreSQL + LLMs. You MUST follow these rules:**
1. Always teach **step-by-step** in **small, easy English**.
2. Frequently use **Laravel analogies** (Eloquent, Migrations, Form Requests, Controllers) to explain new Python/FastAPI concepts.
3. Stop and wait for the user to complete each step before giving the next one.
4. **Current Status:** The user has completed FastAPI Basics, PostgreSQL CRUD, Project Refactoring, and GenAI Phase 1 (System Prompts, Structured Output, Few-Shot Prompting).
5. **Resume point:** The user is currently on **Phase 2: RAG & Embeddings (Task 1: Testing `/notes/ai/embed`, then Task 2: pgvector setup)**. See `pending_tasks.md` for the exact code and next steps!

---

## 🧭 Master Progress Tracker

### ✅ Module 1: FastAPI Fundamentals
- [x] Create virtual environment and install FastAPI/Uvicorn
- [x] Basic routing (`@app.get("/")`)
- [x] Pydantic data validation (`BaseModel`)
- [x] Swagger auto-documentation (`/docs`)

### ✅ Module 2: PostgreSQL Database & CRUD
- [x] Connect async database (`asyncpg` + `SQLAlchemy`)
- [x] Create database models (`models.py`)
- [x] Auto-table creation with modern `lifespan` event
- [x] Full CRUD operations (Create, Read all, Read by ID, Update, Delete)
- [x] Database dependency injection with `Depends(get_db)`

### ✅ Module 3: Production Project Refactoring
- [x] Separate Pydantic schemas into `schemas.py`
- [x] Separate endpoints into `routers/notes.py` using `APIRouter`
- [x] Secure API keys using `.env` and `python-dotenv`
- [x] Clean, scalable architecture matching real-world company standards

### ✅ Module 4: GenAI Phase 1 (LLM Control)
- [x] Connect Google Gemini API (`gemini-3.8-flash`)
- [x] System Prompts / Instructions (giving AI roles & personalities)
- [x] Structured Output (forcing AI to return valid Pydantic JSON)
- [x] Few-Shot Prompting (training the model with input/output examples)

---

### ⏳ Module 5: GenAI Phase 2 (RAG & Embeddings) — CURRENT FOCUS
- [x] **Task 1:** Test text embeddings using `gemini-embedding-001` (Route: `POST /notes/ai/embed`)
- [x] **Task 2:** Install `pgvector` in PostgreSQL (`CREATE EXTENSION vector;`) and in Python (`pip install pgvector`)
- [x] **Task 3:** Add vector column to `models.py` and store embeddings in PostgreSQL
- [ ] **Task 4:** Build "Semantic Search / Chat with My Notes" (Full RAG endpoint)

---

### 🔮 Module 6: GenAI Phase 3 (AI Agents & Function Calling) — UPCOMING
- [ ] Understand Function Calling / Tools
- [ ] Create Python tools the AI can execute autonomously (e.g. weather search, database lookups)
- [ ] Build a fully autonomous GenAI Assistant
