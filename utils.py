import os

def videoId(filepath):
    """Extracts the video_id from '<scope>_<video_id>.<ext>' filenames."""
    name = os.path.basename(filepath)              # audio_abc123.mp3
    name_without_ext = os.path.splitext(name)[0]   # audio_abc123

    parts = name_without_ext.split("_", 1)         # ["audio", "abc123"]

    if len(parts) > 1:
        return parts[1]                            # abc123
    else:
        return None

def standard_filename(video_id, filename):
    base_dir = os.path.join("resources", video_id)
    os.makedirs(base_dir, exist_ok=True)
    
    return os.path.join(base_dir, filename)
