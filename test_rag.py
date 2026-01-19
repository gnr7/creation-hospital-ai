# test_rag.py
from rag.retriever import retrieve_context

query = "hospital ka opd timing kya hai?"
context = retrieve_context(query)

print("Retrieved Context:")
print(context)
