from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Mengambil API key dari environment variable
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt", "")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "google/gemma-3n-e2b-it:free",  # Model aman dan sering berhasil
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        result = response.json()

        # Cek apakah respons mengandung "choices"
        if "choices" in result:
            return jsonify({"answer": result["choices"][0]["message"]["content"]})
        else:
            return jsonify({"error": result})  # tampilkan error dari OpenRouter
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return jsonify({"message": "OpenRouter Flask API running!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # untuk Railway
    app.run(host="0.0.0.0", port=port)


