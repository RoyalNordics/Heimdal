from flask import Flask, request, jsonify
import openai
import sqlite3
import requests
import os

app = Flask(__name__)

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = "https://heimdal.onrender.com"
DATABASE_PATH = "autosome.db"

# Initialize OpenAI
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Please set OPENAI_API_KEY environment variable.")
openai.client = openai.OpenAI(api_key=OPENAI_API_KEY)

def init_db():
    """Initialize database if not exists."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        occasion TEXT,
                        audience TEXT,
                        generated_text TEXT,
                        generated_media TEXT,
                        suggested_hashtags TEXT,
                        recommended_platforms TEXT,
                        best_posting_time TEXT,
                        strategy_suggestions TEXT,
                        edited_text TEXT,
                        selected_media TEXT,
                        status TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return "Webhook is running!"

@app.route('/api/generate_post', methods=['POST'])
def generate_post():
    """Generate a post using GPT-4."""
    try:
        data = request.json
        print("Received data:", data)  # Debugging
        
        if not data or 'post_title' not in data or 'post_occasion' not in data or 'target_audience' not in data:
            raise ValueError("Missing required fields in request data")

        prompt = f"""
        Generate a social media post based on:
        - Title: {data['post_title']}
        - Occasion: {data['post_occasion']}
        - Audience: {data['target_audience']}
        """
        print("Generated prompt:", prompt)  # Debugging

        response = openai.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        generated_text = response.choices[0].message.content
        print("Generated text:", generated_text)  # Debugging

        # Store post in database
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO posts (title, occasion, audience, generated_text, status)
                          VALUES (?, ?, ?, ?, ?)''', 
                          (data['post_title'], data['post_occasion'], data['target_audience'], generated_text, 'Draft'))
        conn.commit()
        post_id = cursor.lastrowid
        conn.close()
        
        return jsonify({"post_id": post_id, "generated_text": generated_text})
    
    except Exception as e:
        print("Error in generate_post:", str(e))  # Debugging
        return jsonify({"error": str(e)}), 500

@app.route('/api/update_post', methods=['POST'])
def update_post():
    """Update an existing post with edited text and selected media."""
    data = request.json
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''UPDATE posts SET edited_text = ?, selected_media = ?, status = ? WHERE id = ?''',
                   (data['edited_text'], data['selected_media'], data['status'], data['post_id']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Post updated successfully"})

@app.route('/api/post_to_platform', methods=['POST'])
def post_to_platform():
    """Send post data to webhook for publishing."""
    data = request.json
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Post sent to webhook", "response": response.text})

@app.route('/api/get_post_metrics', methods=['GET'])
def get_post_metrics():
    """Retrieve post performance data."""
    post_id = request.args.get('post_id')
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM posts WHERE id = ?''', (post_id,))
    post = cursor.fetchone()
    conn.close()
    if post:
        return jsonify({"post": post})
    return jsonify({"message": "Post not found"}), 404

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))  # Use Render's dynamic port
    print("Starting Flask on port", port)
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(rule)
    app.run(debug=True, host='0.0.0.0', port=port)