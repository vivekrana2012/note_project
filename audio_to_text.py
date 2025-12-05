from utils import videoId, standard_filename
from faster_whisper import WhisperModel
from prefect import task

@task
def transcript(filename):
    model = WhisperModel("small")

    segments, info = model.transcribe(filename)

    video_id = videoId(filename)

    transcript_filename = standard_filename(video_id, f"transcript__{video_id}.txt")

    # Open the output file for writing
    with open(transcript_filename, "w", encoding="utf-8") as f:
        for seg in segments:
            f.write(seg.text + "\n")

    print(f"Transcription saved to {transcript_filename}")

    return transcript_filename
