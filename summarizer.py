from utils import videoId, standard_filename
import ollama
from prefect import task
import os

# ----------------------------
# CHUNKING WITH OVERLAP
# ----------------------------
def chunk_text(text, max_words=500, overlap_words=100):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + max_words
        chunk = words[start:end]
        chunks.append(" ".join(chunk))
        start = end - overlap_words
    
    return chunks


# ----------------------------
# CALL OLLAMA MODEL (LOCAL API)
# ----------------------------
def run_ollama(model, prompt):
    response = ollama.generate(model=model, prompt=prompt, stream=False)
    return response["response"].strip()


def build_merge_prompt(summary_a, summary_b):
    return f"""
        You are an expert technical summarizer.

        Your job is to MERGE two summaries into ONE final summary.

        RULES:
        - Group the information by entity.
        - Do NOT mix unrelated entities.
        - If the same entity appears in both summaries, merge their information.
        - Preserve ALL numbers exactly as written (no rounding, no rewriting).
        - Do not drop any important facts.
        - Maintain the exact structure shown below.
        - Don't include any notes or explainations.

        OUTPUT FORMAT (follow exactly):

        ### ENTITY_NAME
        - <STATEMENT1>
        - <STATEMENT2>

        Repeat this structure for every entity.

        SUMMARY A:
        {summary_a}

        SUMMARY B:
        {summary_b}
        """


def merge_all_chunk_summaries(model, chunk_summaries):
    # Start with the first summary
    merged = chunk_summaries[0]

    for i in range(1, len(chunk_summaries)):
        current = chunk_summaries[i]

        prompt = build_merge_prompt(merged, current)
        
        print(f"Merging chunk {i}...")

        merged = run_ollama(model, prompt).strip()

    return merged

@task
def summarize(filename):

    if not os.path.exists(filename):
        raise FileNotFoundError(f"Transcript file not found: {filename}")

    model = "llama3.2:3b"

    with open(filename, "r", encoding="utf-8") as f:
        transcript = f.read()

    chunks = chunk_text(transcript, max_words=500, overlap_words=100)
    print(f"Total chunks: {len(chunks)}\n")

    chunk_summaries = []

    # ----------------------------
    # 1 — Summarize each chunk (with number preservation)
    # ----------------------------
    for i, chunk in enumerate(chunks):
        print(f"Summarizing chunk {i+1}/{len(chunks)}...")

        prompt = f"""

            You are an expert technical summarizer.

            Your primary objective: Extract and preserve ALL numeric information exactly as stated.

            TASK:
            Given a text containing multiple topics or entities, rewrite it in a structured format where:
            - Each entity or topic is separated.
            - For each entity, provide:
                1. Entity Name - Identify companies and government/regulatory bodies as ENTITIES. If an entity appears multiple times, merge its info into one json item.
                2. Summary - Keep each summary concise and fully factual. Provide numeric details with FULL CONTEXT. Include every number (dates, amounts, percentages, counts, metrics) and never modify, round, or add numbers.

            OUTPUT FORMAT (STRICT — MUST FOLLOW EXACTLY):

            ### ENTITY_NAME
            - <STATEMENT1>
            - <STATEMENT2>
                
            TRANSCRIPT CHUNK:
            {chunk}
        """

        summary = run_ollama(model, prompt)
        chunk_summaries.append(summary)


    # ----------------------------
    # Save chunk summaries
    # ----------------------------

    video_id = videoId(filename)
    chunk_summaries_filename = standard_filename(video_id, f"chunk_summaries_{video_id}.txt")

    with open(chunk_summaries_filename, "w", encoding="utf-8") as f:
        for i, s in enumerate(chunk_summaries):
            f.write(f"\n\n===== CHUNK {i+1} =====\n{s}\n")

    print(f"Chunk summary saved to {chunk_summaries_filename}")

    # ----------------------------
    # 2 — META SUMMARY (summary of summaries)
    # ----------------------------
    print("\nCreating final summary...\n")

    final_summary = merge_all_chunk_summaries(model, chunk_summaries)

    final_summary_filename = standard_filename(video_id, f"final_summary_{video_id}.txt")

    with open(final_summary_filename, "w", encoding="utf-8") as f:
        f.write(final_summary)

    print(f"Final summary saved to {final_summary_filename}")

    return final_summary
