import os
import requests
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

# Hent GPT API-nøglen fra miljøvariabler
api_key = os.getenv('OPENAI_API_KEY')
gpt_url = "https://api.openai.com/v1/chat/completions"  # Korrekt URL for GPT-4

# Debugging: Log API-nøglen for at sikre, at den er korrekt indlæst
print(f"Using GPT API key: {api_key}")  # For debugging, printer nøglen

def query_gpt(prompt):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    data = {
        'model': 'gpt-4',  # Brug GPT-4 modellen
        'messages': [{'role': 'user', 'content': prompt}],  # Opret en beskedstruktur for chat
        'max_tokens': 100,
    }

    # Debugging: Se hvordan data ser ud, før vi sender det
    print(f"Sending data to GPT: {data}")

    try:
        response = requests.post(gpt_url, json=data, headers=headers)
        print(f"GPT Response: {response.text}")  # Log GPT svar
        response.raise_for_status()  # Hvis der er en HTTP-fejl, vil dette generere en undtagelse
    except requests.exceptions.RequestException as e:
        print(f"Error with GPT API call: {e}")
        return {"error": str(e)}

    return response.json()

@app.route("/")
def home():
    print("Flask home route accessed")  # Log når Flask home route tilgås
    return "Webhook is running!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Log incoming Webhook request
        data = request.get_json(force=True)
        print(f"Received Webhook Data: {data}")

        # Forbered prompt til GPT
        prompt = f"Generate a response based on the following data: {data}"
        gpt_response = query_gpt(prompt)

        # Returner GPT's svar
        return jsonify({"status": "received", "gpt_response": gpt_response}), 200

    except Exception as e:
        # Debugging: Log fejl
        print(f"Error processing webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    try:
        print("Starting Flask app...")  # Log for at bekræfte at Flask starter
        port = int(os.environ.get("PORT", 10000))
        print(f"Flask running on port {port}")  # Log for at sikre, at porten er korrekt
        app.run(host="0.0.0.0", port=port)
    except Exception as e:
        print(f"Error starting Flask server: {str(e)}")  # Log eventuelle fejl under opstart
