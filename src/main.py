import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Webhook server is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Webhook received:", data)  # Debugging output
    return jsonify({"status": "received"}), 200

# 🔍 Debug Endpoint - Bruges til at tjekke om miljøvariablerne er korrekt indlæst
@app.route("/debug_env", methods=["GET"])
def debug_env():
    return jsonify({
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", "Not Found")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
