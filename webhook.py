from flask import Flask, request, jsonify
import threading
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Webhook is running!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Log incoming GitHub Webhook request
        data = request.get_json(force=True)  # Force JSON-parsing
        print("Received GitHub Webhook:", data)

        # Return 200 OK immediately to avoid GitHub timeout
        def process_webhook():
            print("Processing Webhook Data:", data)
        
        threading.Thread(target=process_webhook).start()
        
        return jsonify({"status": "received"}), 200
    except Exception as e:
        print("Error processing webhook:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    # Use Render's PORT environment variable
    port = int(os.environ.get("PORT", 10000))  # Default to 10000 if PORT is not set
    app.run(host="0.0.0.0", port=port)
