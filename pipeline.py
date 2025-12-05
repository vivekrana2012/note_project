from yt_to_audio import download_audio
from audio_to_text import transcript
from summarizer import summarize

from summary_formatter import format

from prefect import task

@task
def yt_pipeline(url: str):
    audio_filename = download_audio(url)

    transcript_filename = transcript(audio_filename)

    summarized_filename = summarize(transcript_filename)

    formatted_filename = format(summarized_filename)

    return {
        "audio": audio_filename,
        "transcript": transcript_filename,
        "summary": summarized_filename,
        "json": formatted_filename
    }