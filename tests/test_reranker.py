from retrieval.retriever import retrieve
from retrieval.reranker import rerank

query="what to do when database connections are exhausted"
docs = retrieve(query=  query,category="incident",k=5)


print("Before Rerank:")
for d in docs:
    print(d.metadata.get("section"))

docs = rerank(query, docs)

print("\nAFTER RERANK:")
for d in docs:
    print(d.metadata.get("section"))
