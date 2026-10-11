# Current & Pending Tasks: Phase 2 (RAG & Embeddings)

*Note to AI Assistant: The user has completed FastAPI basics, CRUD, and GenAI Phase 1 (System Prompts, Structured Output, Few-Shot). They are now learning Phase 2: RAG and Embeddings. Continue from where they left off below in simple English and step-by-step!*

---

### 📖 Concept: What is an "Embedding"? (The Core of AI)
Computers do not understand words; they only understand numbers.
An **Embedding** is a list of decimal numbers (called a **Vector**) that represents the **meaning** of a sentence.

Example:
* `"Puppy"` ➔ `[0.82, -0.15, 0.94, ...]`
* `"Dog"`   ➔ `[0.81, -0.14, 0.93, ...]`
* `"Airplane"` ➔ `[-0.45, 0.90, -0.12, ...]`

Because "Puppy" and "Dog" mean the same thing, their numbers are almost identical! This allows us to do **Semantic Search** (searching by meaning instead of exact keywords).

---

## 📋 Pending Tasks Checklist

### Task 1: Test Generating an Embedding (CURRENT STEP)
1. Add this test route to `routers/notes.py`:
```python
@router.post("/ai/embed")
async def create_embedding(request: schemas.SmartNoteCreate):
    response = ai_client.models.embed_content(
        model='text-embedding-004',
        contents=request.content
    )
    vector = response.embeddings[0].values
    return {
        "text": request.content,
        "total_numbers": len(vector),
        "first_5_numbers": vector[:5]
    }
```
2. Open Swagger UI (`/docs`) and hit `POST /notes/ai/embed`.
3. Give any sample content like:
```json
{
  "content": "FastAPI and PostgreSQL are great for building GenAI applications."
}
```
4. Observe the `total_numbers` (Gemini returns 768 numbers for every sentence!).

---

### Task 2: Understand pgvector in PostgreSQL
* Standard SQL stores strings, integers, and booleans.
* To store a list of 768 numbers (Vectors) and search them at lightning speed, PostgreSQL has an official extension called **`pgvector`**.
* We will install `pgvector` in PostgreSQL and add a `vector` column to our `notes` table.

---

### Task 3: Store Embeddings in the Database
* Whenever a user creates a note, we will automatically generate its Embedding numbers and save them inside PostgreSQL alongside the title and content.

---

### Task 4: Build the "Chat with My Notes" Feature (Full RAG)
* User asks: *"What was that problem I had with the server?"*
* Step 1: Turn the user's question into embedding numbers.
* Step 2: Query PostgreSQL to find the closest matching note using vector math.
* Step 3: Pass that note to Gemini to write a smart, accurate answer!
