import re, json, os
from utils import videoId
import ollama
from prompts import ENTITY_NAME_CLEANER, SUMMARY_POINT_CLEANER
from prefect import task

def run_ollama(model, prompt):
    response = ollama.generate(model=model, prompt=prompt, stream=False)
    return response["response"].strip()

@task
def format(filename):

    if not os.path.exists(filename):
        raise FileNotFoundError(f"Summary file not found: {filename}")

    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()

    sections = re.split(r'^###\s*', text, flags=re.M)
    result = []

    model = "llama3.2:3b"

    for sec in sections:
        sec = sec.strip()
        if not sec: 
            continue
            
        lines = sec.splitlines()
        
        if not lines:
            continue

        # Clean entity name
        entity = run_ollama(model, ENTITY_NAME_CLEANER.format(lines[0].strip()))
        entity = entity.replace("blank", "").strip()
        
        if not entity:
            continue

        # Extract and clean bullet points
        bullets = [re.sub(r'^[-*•]\s*', '', l).strip()
                for l in lines[1:] if re.match(r'^[-*•]', l)]
        
        if not bullets:
            continue
        
        cleaned_bullets = []
        for b in bullets:
            if not b:
                continue
            cleaned = run_ollama(model, SUMMARY_POINT_CLEANER.format(b))
            cleaned = cleaned.replace("blank", "").strip()
            if cleaned:
                cleaned_bullets.append(cleaned)
        
        if cleaned_bullets:
            result.append({"entity": entity, "summary": cleaned_bullets})

    video_id = videoId(filename)
    formatted_filename = os.path.join("resources", video_id, f"formatted_summary__{video_id}.json")

    # Write JSON to file
    with open(formatted_filename, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Formatted summary saved to {formatted_filename}")
    
    return formatted_filename
