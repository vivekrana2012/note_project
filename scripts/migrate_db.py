import sqlite3
import os

db_path = os.path.join("..", "resources", "youtube.db")

conn = sqlite3.connect(db_path)
cur = conn.cursor()

try:
    # Drop the existing table
    cur.execute("DROP TABLE IF EXISTS youtube")
    
    # Recreate with new schema
    cur.execute("""
        CREATE TABLE youtube (
            video_id      TEXT PRIMARY KEY,
            url           TEXT,
            title         TEXT,
            publish_date  TEXT,
            thumbnail     TEXT,
            keywords      TEXT,
            timestamp     TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    print("Table 'youtube' dropped and recreated successfully!")
    
except sqlite3.Error as e:
    print(f"Database error: {e}")
finally:
    conn.close()
