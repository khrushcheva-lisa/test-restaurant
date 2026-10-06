python -m venv .venv 
.venv\Scripts\Activate 
cd backend  
uvicorn app.main:app --reload
http://127.0.0.1:8000/docs
python run_api.py
DATABASE_URL=postgresql://user:password@localhost:port/db