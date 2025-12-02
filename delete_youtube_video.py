import sqlite3
import os
import sys
import shutil

def delete_video(video_id):
    db_path = os.path.join("resources", "youtube.db")
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return False
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    try:
        # Check if video exists
        cur.execute("SELECT video_id, title FROM youtube WHERE video_id=?", (video_id,))
        row = cur.fetchone()
        
        if not row:
            print(f"Video with ID '{video_id}' not found in database.")
            return False
        
        print(f"Found video: {row[1]}")
        
        # Delete from database
        cur.execute("DELETE FROM youtube WHERE video_id=?", (video_id,))
        conn.commit()
        print(f"Deleted video '{video_id}' from database.")
        
        # Delete associated files
        video_dir = os.path.join("resources", video_id)
        if os.path.exists(video_dir):
            shutil.rmtree(video_dir)
            print(f"Deleted directory: {video_dir}")
        
        # Delete metadata file if it exists in root
        metadata_file = f"metadata_{video_id}.txt"
        if os.path.exists(metadata_file):
            os.remove(metadata_file)
            print(f"Deleted metadata file: {metadata_file}")
        
        return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python delete_youtube_video.py <video_id>")
        sys.exit(1)
    
    video_id = sys.argv[1]
    success = delete_video(video_id)
    sys.exit(0 if success else 1)
