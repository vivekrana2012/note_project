CHUNK_SUMMARIZE_PROMPT = """
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

MERGE_SUMMARIES_PROMPT = """
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

ENTITY_NAME_CLEANER = """
Clean up the following entity name. Remove any extra words, symbols, or formatting.
Return ONLY the clean entity name, nothing else.
If the entity name is empty or invalid, return "blank".

Entity name: {0}
"""

SUMMARY_POINT_CLEANER = """
Clean up the following summary point. Remove any extra formatting, symbols, or redundant text.
Make it clear and concise while preserving all numbers and facts exactly as stated.
If the point is empty or invalid, return "blank".

Summary point: {0}
"""