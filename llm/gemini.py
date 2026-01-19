import os
from dotenv import load_dotenv
from google import genai

# Load .env explicitly (REQUIRED for Streamlit)
load_dotenv()

USE_GEMINI = os.getenv("USE_GEMINI", "false").lower() == "true"
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "models/gemini-2.5-flash")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def _deduplicate_context(text: str) -> str:
    """
    Removes repeated lines coming from RAG chunks.
    """
    seen = set()
    cleaned = []

    for line in text.splitlines():
        line = line.strip()
        if line and line not in seen:
            seen.add(line)
            cleaned.append(line)

    return " ".join(cleaned)


def gemini_rewrite(context: str, question: str) -> str:
    """
    Gemini is ONLY used to rewrite and compress RAG output.
    NEVER to add new information.
    """

    if not context.strip():
        return "Sorry, I don’t have this information right now."

    # If Gemini is disabled, return cleaned RAG
    cleaned_context = _deduplicate_context(context)

    if not USE_GEMINI:
        return cleaned_context

    if not GEMINI_API_KEY:
        return cleaned_context

    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""
You are a hospital AI assistant.

STRICT RULES:
- Use ONLY the information provided
- DO NOT repeat sentences
- DO NOT add new facts
- DO NOT mention languages unless asked
- Answer in 1–2 concise sentences

Hospital Information:
{cleaned_context}

User Question:
{question}

Answer (complete sentence, no truncation):
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config={
            "temperature": 0.1,
            "max_output_tokens": 300,
        },
    )

    return response.text.strip()
