import os
import openai
import psycopg2
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Databaseforbindelse
DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def save_to_db(event_type, payload):
    """Gemmer webhook-data i PostgreSQL databasen"""
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
        print(f"❌ Database error: {e}")

def send_to_gpt(webhook_data):
    """Sender webhook-data til GPT-4 for analyse"""
    if not OPENAI_API_KEY:
        print("❌ OpenAI API-nøgle mangler!")
        return
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that analyzes GitHub webhook events."},
                {"role": "user", "content": f"Analyze this event: {webhook_data}"}
            ],
            api_key=OPENAI_API_KEY
        )
        gpt_response = response['choices'][0]['message']['content']
        print(f"✅ GPT Response: {gpt_response}")
    except Exception as e:
        print(f"❌ Fejl ved kald til GPT: {e}")

@app.route("/")
def home():
    return "Middleware is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    """Modtager webhook-event, gemmer det i DB og sender det til GPT"""
    data = request.json
    event_type = request.headers.get("X-GitHub-Event", "unknown")
    
    save_to_db(event_type, data)
    send_to_gpt(data)  # ➡️ Send webhook-data til GPT
    
    return jsonify({"status": "received"}), 200

@app.route("/debug_env", methods=["GET"])
def debug_env():
    """Debug-endpoint til at tjekke miljøvariabler"""
    return jsonify({
        "DATABASE_URL": "Set" if DATABASE_URL else "Not Found",
        "OPENAI_API_KEY": "Set" if OPENAI_API_KEY else "Not Found"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
