import os
from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Databaseforbindelse
DATABASE_URL = os.getenv("DATABASE_URL")

def save_to_db(event_type, payload):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO webhook_events (event_type, payload, created_at) VALUES (%s, %s, %s)",
            (event_type, payload, datetime.utcnow()),
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
    data = request.json
    event_type = request.headers.get("X-GitHub-Event", "unknown")
    
    save_to_db(event_type, data)
    
    return jsonify({"status": "received"}), 200

# 🔍 Debug Endpoint - Bruges til at tjekke om miljøvariablerne er korrekt indlæst
@app.route("/debug_env", methods=["GET"])
def debug_env():
    return jsonify({
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", "Not Found")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
