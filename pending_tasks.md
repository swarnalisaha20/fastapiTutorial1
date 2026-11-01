# Pending Task: Final Capstone Project (Autonomous AI Assistant)

***⚠️ DIRECTIVE FOR ANY AI ASSISTANT ON THE OFFICE COMPUTER ⚠️***
**The user is a Laravel developer learning FastAPI + GenAI. Do NOT modify the code or DB automatically.**
**The user wants to manually type/edit the code themselves on this machine. Guide them step-by-step through the instructions written below.**

---

## 📦 Office Computer Setup (Database & Code)

### How to Restore the Exact Same DB & Notes on the Office Computer:
1. Open pgAdmin at the office.
2. Create an empty database named **`fastapi_ai`**.
3. Open Query Tool on `fastapi_ai` and ensure `vector` is enabled:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
4. Open Query Tool, click the **Open File** icon (folder icon in pgAdmin toolbar), select **`database_backup.sql`** from your cloned folder, and click **Execute (F5)**!
5. All your tables, notes, and 3,072-dimension vector embeddings will be restored 100%!

---

## 🎯 What We Are Building: The Capstone AI Assistant

We are creating an **Autonomous AI Agent** that has **three tools**:
1. `get_current_weather(city: str)` ➔ Returns live weather data.
2. `save_quick_note(title: str, content: str)` ➔ Saves a note directly to PostgreSQL database.
3. `search_database_notes(keyword: str)` ➔ Searches PostgreSQL notes table for relevant records.

When a user chats with `/notes/ai/autonomous-agent`:
* If they ask about the weather ➔ AI automatically calls `get_current_weather`.
* If they say *"Remember that I have a doctor appointment on Friday at 4 PM"* ➔ AI automatically creates a title and calls `save_quick_note` to insert it into PostgreSQL!
* If they ask *"What notes do I have about meetings?"* ➔ AI calls `search_database_notes` and answers from the DB.
* If they just say *"Hello!"* ➔ AI answers normally without calling any tools.

---

## 📝 Step-by-Step Implementation Guide

Follow these 4 steps in order:

---

### Step 1: Add Database Helper Functions in `routers/notes.py`

Open `routers/notes.py`. Right below your existing `get_current_weather` function (around line 35), paste these two database helper tools:

```python
from database import SessionLocal

# Tool 2: Allows the AI to save notes directly to PostgreSQL
async def save_quick_note(title: str, content: str) -> str:
    """Saves a new note to the database with a title and content."""
    async with SessionLocal() as db:
        # Generate embedding vector for the new note
        embed_resp = ai_client.models.embed_content(
            model='gemini-embedding-001',
            contents=content
        )
        vector = embed_resp.embeddings[0].values
        
        new_note = models.Note(title=title, content=content, embedding=vector)
        db.add(new_note)
        await db.commit()
        await db.refresh(new_note)
        return f"Successfully saved note #{new_note.id}: '{new_note.title}'"


# Tool 3: Allows the AI to search database notes
async def search_database_notes(keyword: str) -> str:
    """Searches the database notes by keyword or meaning."""
    async with SessionLocal() as db:
        query = select(models.Note).where(
            models.Note.title.ilike(f"%{keyword}%") | models.Note.content.ilike(f"%{keyword}%")
        ).limit(3)
        result = await db.execute(query)
        notes = result.scalars().all()
        
        if not notes:
            return f"No notes found matching '{keyword}'."
        
        return "\n".join([f"ID: {n.id} | Title: {n.title} | Content: {n.content}" for n in notes])
```

---

### Step 2: Add the Autonomous Agent Route in `routers/notes.py`

Scroll down to the bottom of `routers/notes.py` and paste this new endpoint:

```python
@router.post("/ai/autonomous-agent")
async def autonomous_agent(request: schemas.PromptRequest):
    """
    Autonomous AI Agent with 3 tools:
    1. Weather lookup
    2. Note creation in PostgreSQL
    3. Note search in PostgreSQL
    """
    # 1. Register all 3 tools with Gemini!
    chat = ai_client.chats.create(
        model='gemini-3.8-flash',
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are a smart personal assistant. "
                "You have tools to check weather, save notes to the database, and search notes. "
                "Use the appropriate tool whenever the user's request requires it. "
                "Be friendly and concise."
            ),
            tools=[get_current_weather, save_quick_note, search_database_notes]
        )
    )

    # 2. Send the message - Gemini will automatically call any tool it needs!
    response = chat.send_message(request.message)

    return {"agent_response": response.text}
```

---

### Step 3: Test the 3 Autonomous Scenarios in Swagger UI (`/docs`)

Start the server:
```powershell
uvicorn main:app --reload
```

Go to `http://127.0.0.1:8000/docs` and open **`POST /notes/ai/autonomous-agent`**:

#### Test Scenario A: Weather Tool
Send:
```json
{
  "message": "What is the weather in London right now?"
}
```
*Expected Result:* AI calls `get_current_weather(city='london')` and tells you it is 14°C, Rainy and Windy.

#### Test Scenario B: Note Creation Tool
Send:
```json
{
  "message": "Please save a note for me: I need to buy milk, eggs, and coffee from the supermarket on Sunday."
}
```
*Expected Result:* AI creates a title like "Grocery List" and calls `save_quick_note`. Check pgAdmin or `GET /notes/` — the note will be in your database!

#### Test Scenario C: Note Search Tool
Send:
```json
{
  "message": "Do I have any notes about grocery or shopping?"
}
```
*Expected Result:* AI calls `search_database_notes(keyword='grocery')` and summarizes the note it found in your database!

---

### Step 4: Final Git Sync
Once all 3 scenarios work in Swagger:
```powershell
git add .
git commit -m "Completed Capstone Autonomous Agent with multi-tool calling"
git push
```
