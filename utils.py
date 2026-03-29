import json,re,os
from openai import OpenAI
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="Place your api key here"
)
def call_model(messages):
    return client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=messages
    )
def clean_output(text):
    return text.replace("```json", "").replace("```", "").strip()
def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    return json.loads(match.group())
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
def clean_output(text: str) -> str:
    """Remove markdown or code block wrappers from model output."""
    return text.replace("```json", "").replace("```", "").strip()
def extract_json(text: str) -> dict:
    """Extract JSON object from string output."""
    match=re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError("Invalid JSON in model output")
