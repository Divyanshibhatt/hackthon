import json
import re
import os
from openai import OpenAI


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="Place your api key here"  #use your own api key
)

PRIMARY_MODEL = "openai/gpt-4o-mini"
FALLBACK_MODEL = "openai/gpt-4o-mini:free"

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

def clean_output(text):
    return text.replace("```json", "").replace("```", "").strip()

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError("Invalid JSON")

def generate_post(topic, mode="professional", lang="both", length="medium"):

    length_map = {
        "short": "80-120 words",
        "medium": "150-220 words",
        "long": "250-350 words"
    }

    if lang == "english":
        output_fields = '"content": "string"'
    elif lang == "hinglish":
        output_fields = '"hinglish": "string"'
    else:
        output_fields = '"content": "string", "hinglish": "string"'

    prompt = f"""
You are a top LinkedIn content strategist.

Write a HIGH-QUALITY LinkedIn post about: {topic}

Tone: {mode}
Length: {length_map[length]}

Rules:
- Strong hook
- Short paragraphs
- 1-2 emojis
- Add 3-5 hashtags
- Human tone

"""

    if lang in ["hinglish", "both"]:
        prompt += "\nAlso convert the SAME post into Hinglish.\n"

    prompt += f"""
Return STRICT JSON:
{{
  "status": "Approved",
  {output_fields}
}}
"""

    response = call_model([{"role": "user", "content": prompt}])
    raw = clean_output(response.choices[0].message.content.strip())

    try:
        result = json.loads(raw)
    except:
        result = extract_json(raw)

    return result


def generate_batch(topic, mode, lang, n, length):
    return [generate_post(topic, mode, lang, length) for _ in range(n)]
