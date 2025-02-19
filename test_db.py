import os
import psycopg2
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://heimdal_db_user:cZvIm8XRLIrelCLE064I8a8mVGhEalLa@dpg-cuqg5gij1k6c73e4ms00-a.frankfurt-postgres.render.com/heimdal_db")

def test_db_insert():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO webhook_events (event_type, payload, created_at) VALUES (%s, %s, %s)",
            ("test_event", '{"test": "manual_insert"}', datetime.utcnow()),
        )
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Manual insert successful!")
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    test_db_insert()
