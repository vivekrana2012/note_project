from fastapi import FastAPI
import os, json
import sqlite3
from datetime import datetime

app = FastAPI()
BASE_PATH = "resources"
DB_PATH = os.path.join(BASE_PATH, "youtube.db")

def get_youtube_rows():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT video_id, url, title, thumbnail, keywords, publish_date, timestamp FROM youtube")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/videos")
def list_existing_videos():
    db_rows = get_youtube_rows()
    existing = []

    for row in db_rows:
        video_id = row["video_id"]
        filename = f"formatted_summary__{video_id}.json"
        filepath = os.path.join(BASE_PATH, video_id, filename)

        if os.path.isfile(filepath):
            # include file info
            row["file"] = filename
            row["path"] = f"{video_id}/{filename}"
            existing.append(row)

    # Sort by publish_date descending
    existing.sort(
        key=lambda row: datetime.fromisoformat(row["publish_date"]),
        reverse=True
    )

    return existing

@app.get("/videos/{video_id}")
def get_video_summary(video_id: str):
    filename = f"formatted_summary__{video_id}.json"
    filepath = os.path.join(BASE_PATH, video_id, filename)

    if not os.path.isfile(filepath):
        return {"error": "Summary not found"}

    # Read and return the JSON content
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data