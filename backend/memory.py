# memory.py
import json
import os
from datetime import datetime

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(entry: dict):
    memory = load_memory()
    entry["timestamp"] = datetime.now().isoformat()
    memory.append(entry)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)
