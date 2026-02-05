import math
import requests
from datetime import datetime

def web_search(query: str, max_results: int = 3):
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json", "no_html": 1}
    try:
        data = requests.get(url, params=params, timeout=10).json()
    except:
        return "Search failed."

    results = []
    if data.get("AbstractText"):
        results.append(data["AbstractText"])

    for t in data.get("RelatedTopics", [])[:max_results]:
        if isinstance(t, dict) and t.get("Text"):
            results.append(t["Text"])

    return "\n".join(results) if results else "No reliable result found."

def calculator(expr: str):
    try:
        return str(eval(expr, {"__builtins__": {}}))
    except:
        return "Calculation error."

def get_date():
    return datetime.now().strftime("%A, %d %B %Y")

def get_time():
    return datetime.now().strftime("%I:%M:%S %p")

def get_datetime():
    return datetime.now().strftime("%A, %d %B %Y %I:%M:%S %p")
