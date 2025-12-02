import sqlite3

# Path to your DB file
db_path = "resources/youtube.db"

# Connect to database (creates file if not exists)
conn = sqlite3.connect(db_path)
cur = conn.cursor()

try:
    # Read SQL from file
    with open("init.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()

    # Execute all commands in the file
    cur.executescript(sql_script)

    # Commit changes and close
    conn.commit()
finally:
    conn.close()

print("Database initialized!")
