# rag/vectorstore.py

import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings


DB_DIR = "chroma_db"
DATA_FILE = "hospital_data.json"


def load_documents():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = []

    for section, content in data.items():
        if isinstance(content, list):
            for item in content:
                documents.append(f"{section}: {item}")
        else:
            documents.append(f"{section}: {content}")

    # Deduplicate documents
    return list(dict.fromkeys(documents))


def get_vectorstore():
    embeddings = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    docs = load_documents()

    vectordb = Chroma.from_texts(
        texts=docs,
        embedding=embeddings,
        persist_directory=DB_DIR
    )

    return vectordb
