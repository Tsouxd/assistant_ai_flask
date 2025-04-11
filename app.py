from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)

# Configuration via variables d'environnement
API_KEY = os.getenv("API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-4o-mini"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": os.getenv("APP_URL", "http://localhost:5000"),
        "X-Title": os.getenv("APP_TITLE", "Assistant AI Flask")
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Tu es un assistant utile."},
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        completion = response.json()
        reply = completion["choices"][0]["message"]["content"]
        return jsonify({"response": reply})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e), "details": response.text if 'response' in locals() else None}), 500

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "False") == "True")