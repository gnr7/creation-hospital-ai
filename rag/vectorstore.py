# rag/vectorstore.py
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

from rag.loader import load_hospital_data


def get_vectorstore():
    texts = load_hospital_data()

    embeddings = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vectordb = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        persist_directory="chroma_db"
    )

    return vectordb
