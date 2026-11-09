# 📋 Pending Task: Document RAG — "Chat with Uploaded PDF"

***⚠️ DIRECTIVE FOR ANY AI ASSISTANT ON THE OFFICE COMPUTER ⚠️***
**The user is a Laravel developer transitioning into a Full-Stack Python GenAI Developer.**
**DO NOT modify the code or DB automatically. The user types/edits the code themselves.**
**Guide them step-by-step in simple English with Laravel analogies.**

---

## 🎯 Goal: Build a "Chat with My Uploaded PDF" API

We are creating two new endpoints:
1. `POST /notes/upload-pdf` ➔ User uploads a PDF file. The API reads the text, splits it into paragraph chunks, generates 3,072 vector embeddings, and stores them in PostgreSQL!
2. `POST /notes/ask-pdf` ➔ User asks any question about the uploaded document, and the AI answers based strictly on the PDF!

---

## 📝 Step-by-Step Implementation Guide

Follow these steps in order when you sit at your office computer:

---

### Step 1: Install `pypdf`
Open PowerShell (with your `venv` active) and install the PDF reader:
```powershell
pip install pypdf
```

---

### Step 2: Create a New Model for Document Chunks in `models.py`
Open `models.py`. At the bottom, add a new table model to store pages/chunks of uploaded documents:

```python
class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), index=True)
    chunk_text = Column(Text)
    embedding = Column(Vector(3072), nullable=True)
```

In pgAdmin, create the table directly or let FastAPI lifespan create it:
```sql
CREATE TABLE IF NOT EXISTS document_chunks (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255),
    chunk_text TEXT,
    embedding vector(3072)
);
```

---

### Step 3: Add the PDF Upload Route in `routers/notes.py`
Open `routers/notes.py`. Add these imports at the top:
```python
from fastapi import UploadFile, File
from pypdf import PdfReader
import io
```

*(Laravel analogy: `UploadFile` is just like Laravel's `$request->file('document')`!)*

Now add the upload endpoint to `routers/notes.py`:

```python
@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    """Uploads a PDF, extracts text, chunks it, and saves embeddings into PostgreSQL."""
    
    # 1. Read the uploaded PDF file in memory
    contents = await file.read()
    pdf_reader = PdfReader(io.BytesIO(contents))
    
    saved_chunks_count = 0

    # 2. Loop through each page of the PDF
    for page_num, page in enumerate(pdf_reader.pages):
        text = page.extract_text()
        if not text or not text.strip():
            continue
            
        # 3. Generate vector embedding for this page/chunk
        embed_resp = await ai_client.aio.models.embed_content(
            model='gemini-embedding-001',
            contents=text
        )
        vector = embed_resp.embeddings[0].values
        
        # 4. Save into document_chunks table
        chunk_entry = models.DocumentChunk(
            filename=file.filename,
            chunk_text=text,
            embedding=vector
        )
        db.add(chunk_entry)
        saved_chunks_count += 1
        
    await db.commit()
    
    return {
        "message": f"Successfully processed {file.filename}!",
        "pages_indexed": saved_chunks_count
    }
```

---

### Step 4: Add the "Ask PDF" Endpoint in `routers/notes.py`
Add the question-answering endpoint right below the upload route:

```python
@router.post("/ask-pdf")
async def ask_pdf(query_data: schemas.SearchQuery, db: AsyncSession = Depends(get_db)):
    """Asks questions specifically to your uploaded PDF documents using vector search."""
    
    # 1. Turn user question into 3,072 numbers
    question_embed = await ai_client.aio.models.embed_content(
        model='gemini-embedding-001',
        contents=query_data.question
    )
    q_vector = question_embed.embeddings[0].values
    
    # 2. Vector search in document_chunks table for top 2 relevant pages
    query = (
        select(models.DocumentChunk)
        .where(models.DocumentChunk.embedding.isnot(None))
        .order_by(models.DocumentChunk.embedding.cosine_distance(q_vector))
        .limit(2)
    )
    result = await db.execute(query)
    matching_chunks = result.scalars().all()
    
    if not matching_chunks:
        return {"answer": "No relevant information found in uploaded documents."}
        
    context = "\n\n---\n\n".join([f"Source ({c.filename}):\n{c.chunk_text}" for c in matching_chunks])
    
    # 3. Ask Gemini to answer based strictly on the PDF content
    prompt = f"""
You are an expert document assistant. Answer the user's question using ONLY the following excerpts from their uploaded PDF:

--- DOCUMENT EXCERPTS ---
{context}
-------------------------

Question: {query_data.question}
"""
    response = await ai_client.aio.models.generate_content(
        model='gemini-3.8-flash',
        contents=prompt
    )
    
    return {
        "question": query_data.question,
        "sources": [c.filename for c in matching_chunks],
        "ai_answer": response.text.strip()
    }
```

---

### Step 5: Test in Swagger UI (`/docs`)
1. Open `http://127.0.0.1:8000/docs`.
2. Find `POST /notes/upload-pdf`. Click **Try it out**, choose any `.pdf` on your machine, and click **Execute**.
3. Find `POST /notes/ask-pdf`. Type a question about the PDF you just uploaded and click **Execute**!
