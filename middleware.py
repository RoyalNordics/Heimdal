import os
import json
import openai
from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Databaseforbindelse
DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def save_to_db(event_type, payload):
    """Gemmer webhook-events i databasen"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO webhook_events (event_type, payload, created_at) VALUES (%s, %s, %s)",
            (event_type, json.dumps(payload), datetime.utcnow()),
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")

@app.route("/")
def home():
    return "Middleware is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    """Modtager webhooks og gemmer i databasen"""
    data = request.json
    event_type = request.headers.get("X-GitHub-Event", "unknown")

    save_to_db(event_type, data)

    return jsonify({"status": "received"}), 200

@app.route("/debug_env", methods=["GET"])
def debug_env():
    """Tjekker om miljøvariabler er korrekt indlæst"""
    return jsonify({
        "DATABASE_URL": "Set" if DATABASE_URL else "Not Found",
        "OPENAI_API_KEY": "Set" if OPENAI_API_KEY else "Not Found"
    })

@app.route("/test_openai", methods=["GET"])
def test_openai():
    """Tester om OpenAI API fungerer"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Say 'Hello, Heimdal!'"}]
        )
        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

