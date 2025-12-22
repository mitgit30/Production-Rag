# retrieval/reranker.py

from typing import List
from langchain_core.documents import Document


def rerank(query: str,
documents: List[Document],top_k: int = 5) -> List[Document]:

    query_lower = query.lower()
    scored_docs = []

    for doc in documents:
        score = 0
        meta = doc.metadata

        section = (meta.get("section") or "").lower()
        category = (meta.get("category") or "").lower()


        if any(word in query_lower for word in ["what to do", "how", "fix", "resolve", "mitigate", "restart"]):
            if any(s in section for s in ["step", "steps", "diagnostic", "procedure", "resolution", "rollback", "recovery"]):
                score += 5
            if category == "runbook":
                score += 2

       
        if any(word in query_lower for word in ["error", "issue", "problem", "exhausted", "failure"]):
            if any(s in section for s in ["diagnostic", "troubleshoot", "investigate"]):
                score += 3

        
        if any(word in query_lower for word in ["should", "when", "use"]):
            if "when to use" in section or "when not to use" in section:
                score += 2

        scored_docs.append((score, doc))

    scored_docs.sort(key=lambda x: x[0], reverse=True)

    return [doc for _, doc in scored_docs[:top_k]]
