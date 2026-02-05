import os, json
from dotenv import load_dotenv
from openai import OpenAI
from tools import web_search, calculator, get_date, get_time, get_datetime

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

SYSTEM = """
You are an agentic AI.

Rules:
- DATE -> get_date
- TIME -> get_time
- DATE+TIME -> get_datetime
- Math -> calculator
- Facts -> web_search

Output ONLY JSON tool call or:
FINAL: answer

Tools:
web_search(query)
calculator(expr)
get_date()
get_time()
get_datetime()
"""

def ask(messages):
    r = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0
    )
    return r.choices[0].message.content.strip()

def agent_loop(user_input: str):
    g = user_input.lower()

    # -------- FAST LOCAL ROUTING --------
    if "date" in g and "time" not in g:
        return get_date()

    if "time" in g and "date" not in g:
        return get_time()

    if "date" in g and "time" in g:
        return get_datetime()

    msgs = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user_input}
    ]

    while True:
        out = ask(msgs)

        # FINAL text
        if out.startswith("FINAL:"):
            return out.replace("FINAL:", "").strip()

        # python_tag style (extra safety)
        if "<|python_tag|>" in out and "web_search" in out:
            try:
                q = out.split('query="')[-1].split('"')[0]
                return web_search(q)
            except:
                return out

        # Normal text fallback
        if not out.strip().startswith("{"):
            return out
        # -------- SAFE JSON PARSE --------
        try:
            data = json.loads(out)
        except:
            return out
# ----- SUPPORT BOTH FORMATS -----
# Format A: {"tool": "...", "args": {...}}
        if "tool" in data:
            tool = data.get("tool")
            args = data.get("args", {})

# Format B: {"type":"function","name":"calculator","parameters":{...}}
        elif "name" in data and "parameters" in data:
            tool = data.get("name")
            args = data.get("parameters", {})

        else:
    # Not a tool call, treat as normal answer
            return out
        # -------- TOOL EXECUTION --------
        if tool == "web_search":
            return web_search(args.get("query", ""))

        if tool == "calculator":
            return calculator(args.get("expr", ""))

        if tool == "get_date":
            return get_date()

        if tool == "get_time":
            return get_time()

        if tool == "get_datetime":
            return get_datetime()

        # Unknown tool fallback
        return out

