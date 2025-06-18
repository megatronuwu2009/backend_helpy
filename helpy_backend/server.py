from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai

app = Flask(__name__)
CORS(app)

# Set OpenRouter API key
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.base_url = "https://openrouter.ai/api/v1"

@app.route("/")
def home():
    return "Helpy is running!"

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        response = openai.chat.completions.create(
            model="openrouter/openchat",
            messages=[
                {"role": "system", "content": "You are Helpy, a retro terminal assistant who can both chat and execute ideas in plain English."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=200,
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
