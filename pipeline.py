from yt_to_audio import download_audio
from audio_to_text import transcript
from summarizer import summarize

from prefect import flow

@flow(name="YouTube Video to Summary Pipeline", log_prints=True)
def yt_pipeline(url: str):

    audio_filename = download_audio(url)

    transcript_filename = transcript(audio_filename)

    summarized_filename = summarize(transcript_filename)

    return {
        "audio": audio_filename,
        "transcript": transcript_filename,
        "summary": summarized_filename,
    }