from flask import Flask, request, jsonify
import openai
import psycopg2
import requests
import os

app = Flask(__name__)

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = "https://heimdal.onrender.com"
POSTGRES_URL = os.getenv("POSTGRESQL_URL")

# Initialize OpenAI
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Please set OPENAI_API_KEY environment variable.")
openai.client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_db_connection():
    """Create a new database connection."""
    return psycopg2.connect(POSTGRES_URL, sslmode='require')

def init_db():
    """Initialize PostgreSQL database and ensure 'posts' table exists."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
                            id SERIAL PRIMARY KEY,
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
        cursor.close()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print("Error initializing database:", str(e))

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

        # Store post in PostgreSQL database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO posts (title, occasion, audience, generated_text, status)
                          VALUES (%s, %s, %s, %s, %s) RETURNING id''', 
                          (data['post_title'], data['post_occasion'], data['target_audience'], generated_text, 'Draft'))
        post_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"post_id": post_id, "generated_text": generated_text})
    
    except Exception as e:
        print("Error in generate_post:", str(e))  # Debugging
        return jsonify({"error": str(e)}), 500

@app.route('/api/get_post_metrics', methods=['GET'])
def get_post_metrics():
    """Retrieve post performance data."""
    post_id = request.args.get('post_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM posts WHERE id = %s''', (post_id,))
    post = cursor.fetchone()
    cursor.close()
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
