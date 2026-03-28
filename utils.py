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
