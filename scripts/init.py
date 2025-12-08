import sqlite3
import os

# Path to your DB file (parent directory)
db_path = os.path.join("..", "resources", "youtube.db")

# Connect to database (creates file if not exists)
conn = sqlite3.connect(db_path)
cur = conn.cursor()

try:
    # Read SQL from file in same directory
    sql_file = os.path.join(os.path.dirname(__file__), "init.sql")
    with open(sql_file, "r", encoding="utf-8") as f:
        sql_script = f.read()

    # Execute all commands in the file
    cur.executescript(sql_script)

    # Commit changes and close
    conn.commit()
finally:
    conn.close()

print("Database initialized!")
