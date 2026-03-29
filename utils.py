import json
import re
import os
from openai import OpenAI

# ⚠️ Make sure to set your API key here or via environment variable
# Example: os.environ["OPENAI_API_KEY"] = "your_api_key_here"
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  # must be set in environment
    base_url="https://openrouter.ai/api/v1"  # optional if using OpenRouter
)

def call_model(messages):
    """Call the OpenAI chat model and return response"""
    return client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=messages
    )

def clean_output(text):
    """Remove ```json or ``` if present"""
    return text.replace("```json", "").replace("```", "").strip()

def extract_json(text):
    """Extract JSON from string and return as dict"""
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return json.loads(match.group())
    else:
        raise ValueError("No JSON found in model output")
