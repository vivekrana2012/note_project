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

def delete_all_videos():
    db_path = os.path.join("resources", "youtube.db")
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return False
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    try:
        # Get all video IDs
        cur.execute("SELECT video_id, title FROM youtube")
        rows = cur.fetchall()
        
        if not rows:
            print("No videos found in database.")
            return True
        
        print(f"Found {len(rows)} videos in database.")
        print("\nVideos to be deleted:")
        for video_id, title in rows:
            print(f"  - {video_id}: {title}")
        
        # Confirm deletion
        confirm = input(f"\nAre you sure you want to delete ALL {len(rows)} videos? (yes/no): ")
        if confirm.lower() not in ['yes', 'y']:
            print("Deletion cancelled.")
            return False
        
        # Delete all from database
        cur.execute("DELETE FROM youtube")
        conn.commit()
        print(f"\nDeleted all {len(rows)} videos from database.")
        
        # Delete all video directories
        resources_dir = "resources"
        deleted_dirs = 0
        
        for video_id, _ in rows:
            video_dir = os.path.join(resources_dir, video_id)
            if os.path.exists(video_dir):
                shutil.rmtree(video_dir)
                deleted_dirs += 1
                print(f"Deleted directory: {video_dir}")
        
        print(f"\nTotal directories deleted: {deleted_dirs}")
        return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:")
        print("  Delete single video: python delete_youtube_video.py <video_id>")
        print("  Delete all videos:   python delete_youtube_video.py --all")
        sys.exit(1)
    
    arg = sys.argv[1]
    
    if arg == "--all":
        success = delete_all_videos()
    else:
        success = delete_video(arg)
    
    sys.exit(0 if success else 1)
