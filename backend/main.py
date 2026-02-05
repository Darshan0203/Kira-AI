from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import agent_loop
import json
import os
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

HISTORY_FILE = "history.json"

class Prompt(BaseModel):
    message: str

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_history(user, ai):
    history = load_history()
    history.append({
        "user": user,
        "ai": ai,
        "time": datetime.now().isoformat()
    })
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

@app.post("/chat")
def chat(p: Prompt):
    answer = agent_loop(p.message)
    save_history(p.message, answer)
    return {"answer": answer}

@app.get("/history")
def history():
    return load_history()
