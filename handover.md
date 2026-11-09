# 🧠 SESSION HANDOVER: CONTINUOUS MEMORY & NEXT STEP

***⚠️ ATTENTION TO ANY AI ASSISTANT READING THIS (HOME OR OFFICE) ⚠️***
**The user is a Laravel developer transitioning into a Full-Stack Python GenAI Developer.**
**DO NOT ask the user to explain their background, setup, or history. Everything is documented here.**

---

## 👤 User Profile & Teaching Rules
1. **Background:** 2.5 years in Laravel (PHP) + 2 months Django. Strong grasp of MVC, migrations, Eloquent, Form Requests, and controllers.
2. **Current Level:** Finished FastAPI fundamentals, async CRUD, modular project refactoring, and **GenAI Phases 1, 2, and 3**!
3. **Teaching Style:**
   - Speak in **simple, easy English**.
   - Teach **step-by-step**; do NOT give massive code dumps at once.
   - Always use **Laravel analogies** when introducing new concepts.
   - Wait for the user to finish each step before giving the next.
   - **Do NOT modify code or DB automatically without asking** — guide the user to make the changes so they learn.

---

## 🏆 Current Progress & What Has Been Built

### Completed Milestones:
* ✅ **FastAPI & Async:** Virtual environment, Uvicorn, asyncpg + SQLAlchemy async engine, Lifespan auto-table creation, Dependency Injection (`Depends(get_db)`).
* ✅ **Clean Architecture:** `main.py`, `routers/notes.py`, `schemas.py`, `models.py`, `database.py`, hidden `.env` with `python-dotenv`.
* ✅ **Google GenAI Integration:** `gemini-3.8-flash` via `google-genai` SDK using non-blocking async (`ai_client.aio`).
* ✅ **Prompting Mastery:** System Prompts (Pirate mode), Structured Output (Pydantic schema JSON extraction), Few-Shot Prompting (Ticket classifier).
* ✅ **Vector Database & RAG:** PostgreSQL with `pgvector`, 3,072-dimension embeddings (`gemini-embedding-001`), cosine distance search (`<=>`), `/notes/ai/ask-notes` (Semantic Search RAG).
* ✅ **Autonomous AI Agent:** Multi-tool Agent with Async Function Calling (`/notes/ai/autonomus-agent`) with 3 tools:
  1. `get_current_weather(city)` (External tool simulation)
  2. `save_quick_note(title, content)` (Live PostgreSQL insert with vector embedding)
  3. `search_database_notes(keyword)` (PostgreSQL text & title search)

---

## 🎯 EXACT NEXT TOPIC TO START: "Chat with Uploaded PDF" (Document RAG)

The user has decided to prepare for **Remote & Kolkata Python/GenAI developer jobs**.
The single most requested skill in interviews right now is **Document RAG (Chat with PDF)**.

### Immediate Next Tasks for the AI to guide the user through:
See `pending_tasks.md` for full step-by-step code!
1. **Step 1:** Install `pypdf` (`pip install pypdf` and update `requirements.txt`).
2. **Step 2:** Add `DocumentChunk` model in `models.py` for storing document chunks and embeddings.
3. **Step 3:** Add `POST /notes/upload-pdf` endpoint in `routers/notes.py` using `UploadFile` (like Laravel's `$request->file()`).
4. **Step 4:** Add `POST /notes/ask-pdf` endpoint in `routers/notes.py` to search document embeddings and generate answers.
5. **Step 5:** Test uploading and querying a real PDF in Swagger UI!


---

## 🔄 How the User Syncs Between Home & Office

* **When leaving ANY computer:**
  ```powershell
  git add .
  git commit -m "Sync progress"
  git push
  ```
* **When arriving at the other computer:**
  ```powershell
  git pull
  ```
  And simply prompt the AI: **"I pulled the latest code. Read `handover.md` and tell me what is the next step!"**
