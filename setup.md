# Office Computer Setup Guide

Follow this quick guide when you sit at your office computer to get your FastAPI + GenAI project running with the exact same database and code in less than 5 minutes!

---

## 🔑 Things to Have Ready
1. Your **Google Gemini API Key** (from [Google AI Studio](https://aistudio.google.com/app/apikey)).
2. Your PostgreSQL username & password on the office machine.

---

## 🛠️ Step 1: Clone the Repository
Open PowerShell and run:
```powershell
git clone https://github.com/swarnalisaha20/fastapiTutorial1.git
cd fastapiTutorial1
```

---

## 🐍 Step 2: Set Up Python Environment
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🔐 Step 3: Create the `.env` File
Create a new file named exactly `.env` in the root of the project folder:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

---

## 🐘 Step 4: Restore the Exact Database & Data (PostgreSQL)

1. Open **pgAdmin** on your office computer.
2. If `pgvector` is not yet installed on this PostgreSQL:
   * Download precompiled binaries: [andreiramani/pgvector_pgsql_windows Releases](https://github.com/andreiramani/pgvector_pgsql_windows/releases).
   * Copy `lib`, `share`, and `include` into `C:\Program Files\PostgreSQL\17` (or your PostgreSQL version folder).
3. Create a new empty database:
   * Right-click **Databases** ➔ **Create** ➔ **Database**.
   * Database Name: **`fastapi_ai`**
4. Open the **Query Tool** on `fastapi_ai` and enable the vector extension:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
5. Restore all your previous notes & embeddings:
   * Click the **"Open File"** icon (folder icon in the pgAdmin Query Tool toolbar).
   * Select **`database_backup.sql`** from your cloned project folder.
   * Press **Execute (F5)**!
   * *All tables, previous notes, and 3,072 vector embeddings are now 100% restored!*

---

## ⚙️ Step 5: Check `database.py` Credentials
Open `database.py`. Look at line 7:
```python
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/fastapi_ai"
```
* If your PostgreSQL password on the office machine is different (e.g., `root`, `admin`, or `password`), update the password in that string so FastAPI can connect.

---

## 🚀 Step 6: Start the Server & Begin Coding!
Start the FastAPI server:
```powershell
uvicorn main:app --reload
```

Open Swagger UI in your browser:
👉 **http://127.0.0.1:8000/docs**

---

## 🎯 Next Coding Task:
Open **`pending_tasks.md`** and start building the final **Capstone Autonomous AI Assistant**!
