from pytubefix import YouTube
from prefect import task

from utils import standard_filename

import sqlite3
import os
import json

class VideoAlreadyExists(Exception):
    pass

@task
def download_audio(url):

    db_path = os.path.join("resources", "youtube.db")

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    try:
        yt = YouTube(url)
        video_id = yt.video_id

        cur.execute("SELECT 1 FROM youtube WHERE video_id=?", (video_id,))
        exists = cur.fetchone() is not None

        if exists:
            print(f"video {video_id} already exists.")
            raise VideoAlreadyExists(f"video {video_id} already exists.")

        audio_stream = yt.streams.filter(only_audio=True).first()
        
        if not audio_stream:
            raise ValueError("No audio stream available for this video")

        filename = f"audio_{video_id}"

        # Download audio
        out_file = audio_stream.download(output_path=f"./resources/{video_id}", filename=filename)
        print("Downloaded Audio: ", out_file)

        # ---- Create metadata file ----
        metadata_filename = standard_filename(video_id, f"metadata_{video_id}.txt")

        metadata = {
            "video_id": video_id,
            "url": url,
            "title": yt.title,
            "author": yt.author,
            "publish_date": str(yt.publish_date) if yt.publish_date else "Unknown",
            "length_seconds": yt.length,
            "views": yt.views,
            "description": yt.description,
            "thumbnail": yt.thumbnail_url if hasattr(yt, 'thumbnail_url') else None,
            "keywords": yt.keywords if yt.keywords else [],
        }

        with open(metadata_filename, "w", encoding="utf-8") as f:
            for key, value in metadata.items():
                f.write(f"{key}: {value}\n")

        print("Saved metadata: ", metadata_filename)

        # Convert keywords list to JSON string for database
        keywords_json = json.dumps(metadata['keywords'])

        cur.execute("""
        INSERT OR IGNORE INTO youtube (video_id, url, title, publish_date, thumbnail, keywords)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (metadata['video_id'], metadata['url'], metadata['title'], metadata['publish_date'], metadata['thumbnail'], keywords_json))

        conn.commit()
        
        return out_file
        
    finally:
        conn.close()
