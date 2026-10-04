# Pending Tasks to Finish

You still need to add the AI "Smart Notes" feature and hide your API key before pushing to GitHub. Here is exactly what to do step-by-step when you are ready to continue:

### 1. Add the Smart Note Code
Open `main.py` and paste this code at the bottom. This will automatically generate a title using AI before saving it to PostgreSQL!

```python
# 1. New Pydantic Model (User only sends content now!)
class SmartNoteCreate(BaseModel):
    content: str

# 2. The Smart Note Route
@app.post("/smart-notes/")
async def create_smart_note(request: SmartNoteCreate, db: AsyncSession = Depends(get_db)):
    
    # Step A: Ask the AI to generate a title
    prompt = f"Please read this note and generate a short, 3-word title for it. Here is the note: {request.content}"
    
    ai_response = ai_client.models.generate_content(
        model='gemini-3.8-flash',
        contents=prompt,
    )
    
    # Clean up the AI's answer (remove extra spaces or newlines)
    generated_title = ai_response.text.strip()
    
    # Step B: Save it to PostgreSQL! (Using the AI's title and the User's content)
    new_note = models.Note(title=generated_title, content=request.content)
    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    
    return {
        "message": "Smart Note saved successfully!", 
        "note": new_note
    }
```

---

### 2. Hide Your API Key (Using a `.env` file)
Never upload your API key to GitHub! We will use the exact same tool Laravel uses (`.env`).

**A. Install the package:**
Stop your server and run this command:
```powershell
pip install python-dotenv
```

**B. Create the `.env` file:**
Create a new file named exactly `.env` in your folder. Paste your key inside it:
```env
GEMINI_API_KEY=your_actual_long_api_key_here
```

**C. Update `main.py` to read the key:**
At the top of `main.py`, add these imports:
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Tells Python to read the .env file!
```

Change your AI client code so it grabs the hidden key securely:
```python
ai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
```

---

### 3. Push to GitHub
Now that the key is safe, save your work!
```powershell
git add .
git commit -m "Added Smart Notes and hidden API key"
git push
```

---

### 4. The Very Last Step! (Project Structure)
When you finish all of the above, tell me! We will do the final step of our roadmap: splitting `main.py` into separate folders (like `routers/`, `schemas/`, `models/`) just like a real Laravel app!
