from flask import Flask, request, jsonify
from openai import OpenAI
import json
import re
from datetime import datetime

# -------------------------------
# 🔑 CONFIG
# -------------------------------
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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" 
)

PRIMARY_MODEL = "openai/gpt-4o-mini"
FALLBACK_MODEL = "openai/gpt-4o-mini:free"

# -------------------------------
# 🧠 SAFE MODEL CALL
# -------------------------------
def call_model(messages):
    try:
        return client.chat.completions.create(
            model=PRIMARY_MODEL,
            messages=messages,
            temperature=0.6
        )
    except Exception:
        print("⚠️ Primary failed, switching to fallback...")
        return client.chat.completions.create(
            model=FALLBACK_MODEL,
            messages=messages,
            temperature=0.6
        )

# -------------------------------
# 🧹 CLEANERS
# -------------------------------
def clean_output(text):
    return text.replace("```json", "").replace("```", "").strip()

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError("Invalid JSON")

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'\bn([A-Z#])', r'\n\1', text)
    return text.strip()

# -------------------------------
# 🤖 GENERATION
# -------------------------------
def generate_post(topic, mode="professional", lang="both"):

    if lang == "english":
        output_fields = '"content": "string"'
    elif lang == "hinglish":
        output_fields = '"hinglish": "string"'
    else:
        output_fields = '''
"content": "string",
"hinglish": "string"
'''

    prompt = f"""
You are a professional LinkedIn content creator.

TASK:
Write a LinkedIn post about: {topic}
Tone: {mode}

RULES:
- Strong hook
- Clean formatting
- Short paragraphs
- 1–2 emojis max
- Add 5–8 hashtags
"""

    if lang in ["hinglish", "both"]:
        prompt += """
Also convert the SAME post into Hinglish.

HINGLISH RULES:
- Natural Hinglish (like Indians speak)
- Same meaning
- No weird spacing
"""

    prompt += f"""

OUTPUT STRICT JSON:
{{
  "status": "Approved",
  "compliance_issues": [],
  {output_fields}
}}
"""

    response = call_model([{"role": "user", "content": prompt}])
    raw = clean_output(response.choices[0].message.content.strip())

    try:
        result = json.loads(raw)
    except:
        result = extract_json(raw)

    final = {
        "status": result.get("status", "Approved"),
        "compliance_issues": result.get("compliance_issues", [])
    }

    if "content" in result:
        final["content"] = clean_text(result["content"])

    if "hinglish" in result:
        final["hinglish"] = clean_text(result["hinglish"])

    return final

# -------------------------------
# 🌐 FLASK API
# -------------------------------
app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process():
    data = request.json
    topic = data.get("topic")

    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    try:
        result = generate_post(topic)

        return jsonify({
            "content": result.get("content", ""),
            "hinglish": result.get("hinglish", ""),
            "status": result.get("status", "Approved"),
            "compliance_issues": result.get("compliance_issues", [])
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------------
# 🚀 RUN SERVER
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)