import os
import sys
import uvicorn

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(os.path.dirname(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BACKEND_DIR = os.path.join(BASE_DIR, "backend")

if not os.path.exists(BACKEND_DIR):
    raise FileNotFoundError(f"Не найдена папка backend: {BACKEND_DIR}")

sys.path.insert(0, BACKEND_DIR)
os.chdir(BACKEND_DIR)

uvicorn.run(
    "app.main:app",
    host="127.0.0.1",
    port=8000,
    reload=False
)