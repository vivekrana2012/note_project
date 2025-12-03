import re, json, os

def format(filename):

    if not os.path.exists(filename):
        raise FileNotFoundError(f"Summary file not found: {filename}")

    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()

    sections = re.split(r'^###\s*', text, flags=re.M)
    result = []

    for sec in sections:
        sec = sec.strip()
        if not sec: continue
        lines = sec.splitlines()
        entity = lines[0].strip()
        bullets = [re.sub(r'^[-*•]\s*', '', l).strip()
                for l in lines[1:] if re.match(r'^[-*•]', l)]
        result.append({"entity": entity, "summary": bullets})

    # Write JSON to file
    with open("resources/KRwz80Y3hQk/formatted_summary_KRwz80Y3hQk.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    format('resources/KRwz80Y3hQk/final_summary_KRwz80Y3hQk.txt')
