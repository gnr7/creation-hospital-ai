from rag.retriever import retrieve_context
from llm.gemini import gemini_rewrite


def rag_answer(query: str, language: str = "en") -> str:
    context = retrieve_context(query)

    if not context.strip():
        return "Sorry, I don’t have this information right now."

    return gemini_rewrite(context, query)
