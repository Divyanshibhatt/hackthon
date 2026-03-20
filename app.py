
from flask import Flask, request, jsonify
from openai import OpenAI
from localization_agent import translate_to_hindi
from optimization_agent import analyze_and_optimize

app = Flask(__name__)

client = OpenAI(
    api_key="`AIzaSyChJyrEqhPDv_qqwK_MGsmpZT2XfCApc2w`",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# -------------------------------
# Compliance Function
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


@app.route('/process', methods=['POST'])
def process_content():
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
        issues = check_compliance(content)
        hindi_translation = translate_to_hindi(content)

        return jsonify({
            "generated_content": content,
            "compliance_issues": issues,
            "status": "Approved" if not issues else "Needs Review",
            "hindi_translation": hindi_translation
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# ✅ OPTIMIZE ROUTE (MOVE HERE)
@app.route('/optimize', methods=['POST'])
def optimize_content():
    data = request.json
    generated_content = data.get("generated_content", {})
    product_info = data.get("product_info", "")

    # Convert dict → text
    if isinstance(generated_content, dict):
        generated_content = "\n".join(
            f"{k.upper()}:\n{v}" for k, v in generated_content.items()
        )

    report = analyze_and_optimize(generated_content, product_info)
    return jsonify(report)


# -------------------------------
# Run App (ALWAYS LAST)
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)