import sqlite3
import os

db_path = os.path.join("resources", "youtube.db")

conn = sqlite3.connect(db_path)
cur = conn.cursor()

try:
    # Backup existing data
    cur.execute("SELECT video_id, url, title, publish_date, timestamp FROM youtube")
    existing_data = cur.fetchall()
    
    # Drop and recreate table
    cur.execute("DROP TABLE IF EXISTS youtube")
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
    
    # Restore data with NULL for new columns
    for row in existing_data:
        cur.execute("""
            INSERT INTO youtube (video_id, url, title, publish_date, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, row)
    
    conn.commit()
    print(f"Table migrated successfully! Preserved {len(existing_data)} rows.")
    
except sqlite3.Error as e:
    print(f"Database error: {e}")
    conn.rollback()
finally:
    conn.close()
