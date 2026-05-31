from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os
import sys

sys.path.append(os.path.dirname(__file__))

from database import load_csv_to_db
from agent import run_agent

app = FastAPI(title="Data Insights Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "./data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Serve charts as static files so Streamlit can display them
app.mount("/charts", StaticFiles(directory="./data/charts"), name="charts")

@app.get("/")
def health_check():
    return {"status": "Data Insights Agent running"}

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    """Upload CSV and load into SQLite"""
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    result = load_csv_to_db(file_path)
    return result

@app.post("/ask")
async def ask_question(payload: dict):
    """Run the agent on a natural language question"""
    question = payload.get("question", "")
    if not question:
        return {"error": "No question provided"}

    result = run_agent(question)
    return result