# rag/retriever.py

from rag.vectorstore import get_vectorstore

# Similarity threshold (lower = more strict)
SIMILARITY_THRESHOLD = 0.75


def retrieve_context(query: str, k: int = 4) -> str:
    """
    Retrieve relevant context from ChromaDB using semantic search.
    Allows safe partial-name matches for doctors.
    """

    vectordb = get_vectorstore()

    # Retrieve documents with similarity scores
    docs_with_scores = vectordb.similarity_search_with_score(query, k=k)

    filtered_chunks = []
    query_lower = query.lower()

    for doc, score in docs_with_scores:
        content = doc.page_content.strip()
        content_lower = content.lower()

        # ✅ Doctor-name partial match safeguard
        name_match = (
            "dr." in content_lower
            and any(word in content_lower for word in query_lower.split())
        )

        # Keep chunk if:
        # 1. Semantic similarity is good
        # 2. OR partial doctor-name match is detected
        if score <= SIMILARITY_THRESHOLD or name_match:
            filtered_chunks.append(content)

    # Join retrieved chunks into a single context block
    return "\n".join(filtered_chunks)
