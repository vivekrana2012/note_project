from pytubefix import YouTube
from prefect import task

@task
def download_audio(url):
    yt = YouTube(url)

    audio_stream = yt.streams.filter(only_audio=True).first()

    video_id = yt.video_id

    # Audio filename (no extension needed, pytube adds it)
    filename = f"audio_{video_id}"

    # Download audio
    out_file = audio_stream.download(output_path=".", filename=filename)
    print("Downloaded Audio: ", out_file)

    # ---- Create metadata file ----
    metadata_filename = f"metadata_{video_id}.txt"

    metadata = {
        "video_id": video_id,
        "url": url,
        "title": yt.title,
        "author": yt.author,
        "publish_date": str(yt.publish_date),
        "length_seconds": yt.length,
        "views": yt.views,
        "description": yt.description,
        "rating": yt.rating,
        "keywords": yt.keywords,
    }

    with open(metadata_filename, "w", encoding="utf-8") as f:
        for key, value in metadata.items():
            f.write(f"{key}: {value}\n")

    print("Saved metadata: ", metadata_filename)

    return out_file
