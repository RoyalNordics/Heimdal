import psycopg2
import os

# Database-forbindelsesstreng (erstat med din egen, hvis nødvendig)
DATABASE_URL = "postgresql://heimdal_db_user:cZvIm8XRLIrelCLE064I8a8mVGhEalLa@dpg-cuqg5gij1k6c73e4ms00-a.frankfurt-postgres.render.com/heimdal_db"

try:
    # Opret forbindelse til databasen
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # SQL til at oprette tabellen
    create_table_query = """
    CREATE TABLE IF NOT EXISTS webhook_events (
        id SERIAL PRIMARY KEY,
        event_type TEXT NOT NULL,
        payload JSONB NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # Udfør SQL-kommandoen
    cur.execute(create_table_query)
    conn.commit()

    print("✅ Table 'webhook_events' created successfully!")

    # Luk forbindelsen
    cur.close()
    conn.close()

except Exception as e:
    print("❌ Error: ", e)
