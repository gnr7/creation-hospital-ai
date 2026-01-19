# rag/retriever.py
from rag.vectorstore import get_vectorstore


def retrieve_context(query: str, k: int = 3):
    vectordb = get_vectorstore()
    results = vectordb.similarity_search(query, k=k)

    return "\n".join([doc.page_content for doc in results])
