# llm/gemini.py
from google import genai
from google.oauth2 import service_account

PROJECT_ID = "hospital-ivr-ai"
LOCATION = "us-central1"
SERVICE_ACCOUNT_FILE = "gcp-key.json"

SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]


def gemini_answer(context: str, question: str, language: str = "en") -> str:
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES,
    )

    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION,
        credentials=credentials,
    )

    system_prompt = f"""
You are Creation Hospital’s AI Concierge.

STRICT RULES:
- Answer ONLY using the provided hospital information.
- Do NOT use external or medical knowledge.
- If the answer is not present, say:
  "Sorry, I don’t have that information right now."
- Keep answers short, clear, and helpful.
- Respond in the same language as the user.

Hospital Information:
{context}
"""

    response = client.models.generate_content(
        model="models/gemini-1.5-flash-001",  # ✅ THIS IS THE FIX
        contents=[
            system_prompt,
            f"User Question: {question}"
        ],
        config={
            "temperature": 0.2,
            "max_output_tokens": 256,
        }
    )

    return response.text.strip()
