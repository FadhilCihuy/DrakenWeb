from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Ganti dengan OpenRouter API key kamu
OPENROUTER_API_KEY = "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"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt", "")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "openrouter/openchat",  # atau model lain dari https://openrouter.ai/docs#models
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        result = response.json()

        return jsonify({"answer": result["choices"][0]["message"]["content"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return jsonify({"message": "OpenRouter Flask API running!"})

if __name__ == "__main__":
    app.run(debug=True)
