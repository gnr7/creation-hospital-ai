# rag/rag_engine.py
from rag.retriever import retrieve_context


def rag_answer(query: str) -> str:
    """
    Simple RAG-based answer (no LLM yet).
    Returns retrieved hospital knowledge.
    """

    context = retrieve_context(query)

    if not context.strip():
        return "Sorry, I do not have this information right now."

    return context
