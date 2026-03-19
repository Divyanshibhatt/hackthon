from flask import Flask, request, jsonify
from openai import OpenAI  # Using OpenAI-style SDK for Gemini

app = Flask(__name__)

# Use your Gemini API key and endpoint
client = OpenAI(
    api_key="AIzaSyChJyrEqhPDv_qqwK_MGsmpZT2XfCApc2w",  # Paste your AI Studio key here
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

@app.route('/')
def home():
    return "Backend is running with Gemini!"

@app.route('/generate', methods=['POST'])
def generate_content():
    data = request.json
    product_info = data.get("product_info", "")

    try:
        response = client.chat.completions.create(
            model="gemini-2.5-flash",  # or gemini-2.5-pro
            messages=[
                {"role": "system", "content": "You are a professional content writer."},
                {"role": "user", "content": f"Write a LinkedIn post about this product:\n{product_info}"}
            ]
        )
        return jsonify({"content": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)