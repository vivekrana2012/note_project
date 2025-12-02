import sqlite3
import os

def view_youtube_db():
    db_path = os.path.join("resources", "youtube.db")
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT * FROM youtube")
        rows = cur.fetchall()
        
        if not rows:
            print("No rows found in the youtube table.")
            return
        
        # Get column names
        cur.execute("PRAGMA table_info(youtube)")
        columns = [info[1] for info in cur.fetchall()]
        
        print(f"\nTotal rows: {len(rows)}\n")
        print("-" * 80)
        
        for row in rows:
            for col_name, value in zip(columns, row):
                print(f"{col_name}: {value}")
            print("-" * 80)
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    view_youtube_db()
