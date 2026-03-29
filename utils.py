# utils.py
import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

# -------------------------------
# 🔑 LOAD ENV VARIABLES
# -------------------------------
load_dotenv()  # load .env file
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in .env")

# -------------------------------
# 🔗 OPENAI CLIENT
# -------------------------------
client = OpenAI(api_key=api_key)

PRIMARY_MODEL = "openai/gpt-4o-mini"
FALLBACK_MODEL = "openai/gpt-4o-mini:free"

# -------------------------------
# 🧠 MODEL CALL
# -------------------------------
def call_model(messages):
    try:
        return client.chat.completions.create(
            model=PRIMARY_MODEL,
            messages=messages,
            temperature=0.6
        )
    except Exception:
        return client.chat.completions.create(
            model=FALLBACK_MODEL,
            messages=messages,
            temperature=0.6
        )

# -------------------------------
# 🧹 CLEANERS
# -------------------------------
def clean_output(text: str) -> str:
    """Remove markdown or code block wrappers from model output."""
    return text.replace("```json", "").replace("```", "").strip()

def extract_json(text: str) -> dict:
    """Extract JSON object from string output."""
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError("Invalid JSON in model output")
