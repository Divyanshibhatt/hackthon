from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Gemini setup
client = OpenAI(
    api_key="AIzaSyChJyrEqhPDv_qqwK_MGsmpZT2XfCApc2w",  # change this immediately
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# -------------------------------
# Compliance Function (MUST BE ABOVE ROUTES)
# -------------------------------
def check_compliance(content):
    banned_words = ["guarantee", "instant results", "100% sure"]

    issues = []

    for word in banned_words:
        if word in content.lower():
            issues.append(f"Restricted phrase used: {word}")

    if len(content) < 100:
        issues.append("Content too short")

    return issues

# -------------------------------
# Routes
# -------------------------------

@app.route('/')
def home():
    return "Backend is running with Gemini!"

@app.route('/generate', methods=['POST'])
def generate_content():
    data = request.json
    product_info = data.get("product_info", "")

    try:
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": "You are a professional content writer."},
                {"role": "user", "content": f"Write a LinkedIn post about this product:\n{product_info}"}
            ]
        )

        content = response.choices[0].message.content
        return jsonify({"content": content})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/compliance', methods=['POST'])
def compliance_check():
    data = request.json
    content = data.get("content", "")

    issues = check_compliance(content)

    return jsonify({
        "issues": issues,
        "status": "Approved" if not issues else "Needs Review"
    })

# -------------------------------
# Run App (ONLY ONCE, LAST LINE)
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)