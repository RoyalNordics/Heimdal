import os
import json
from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")

def save_to_db(event_type, payload):
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
        print("✅ Data successfully inserted into DB.")
    except Exception as e:
        print(f"❌ Database error: {e}")

@app.route("/")
def home():
    return "Middleware is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    event_type = request.headers.get("X-GitHub-Event", "unknown")

    print(f"🔹 Received webhook: {json.dumps(data, indent=2)}")
    print(f"🔹 Event Type: {event_type}")

    save_to_db(event_type, data)
    
    print("✅ Webhook processed and saved to DB (if no errors above).")

    return jsonify({"status": "received"}), 200

# 🔍 Debug Endpoint - Check if environment variables are loaded correctly
@app.route("/debug_env", methods=["GET"])
def debug_env():
    return jsonify({
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", "Not Found"),
        "DATABASE_URL": os.getenv("DATABASE_URL", "Not Found")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
