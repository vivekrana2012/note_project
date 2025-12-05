import os

def videoId(filepath):
    name_no_ext = os.path.splitext(os.path.basename(filepath))[0]
    parts = name_no_ext.split("__", 1)
    return parts[1] if len(parts) == 2 else None

def standard_filename(video_id, filename):
    base_dir = os.path.join("resources", video_id)
    os.makedirs(base_dir, exist_ok=True)
    
    return os.path.join(base_dir, filename)
