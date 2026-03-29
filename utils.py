import json, re, os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
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
