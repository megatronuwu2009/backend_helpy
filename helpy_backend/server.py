from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai

app = Flask(__name__)
CORS(app)

# Use your OpenRouter key securely
openai.api_key = os.environ.get("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")
openai.api_base = "https://openrouter.ai/api/v1"

@app.route("/api/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="mistralai/mixtral-8x7b",  # You can change this model
            messages=[
                {"role": "system", "content": "You are Helpy, a helpful, quirky, and responsive AI assistant built into a retro terminal interface."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300
        )
        reply = response.choices[0].message["content"].strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "Helpy backend is running!."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
