# retrieval/reranker.py
# Advanced heuristic reranker with category diversity and intent awareness

from typing import List
from collections import defaultdict
from langchain_core.documents import Document


high_value_sections = ["diagnostic","steps","procedure","resolution","root cause","mitigation","recovery"]


low_value_sections = ["purpose","impact","when to use","when not to use"]


def rerank(query: str,documents: List[Document],top_k: int = 5,max_per_category: int = 3) -> List[Document]:

    query_lower = query.lower()
    scored_docs = []

    for doc in documents:
        score = 0
        meta = doc.metadata

        section = (meta.get("section") or "").lower()
        category = (meta.get("category") or "").lower()

        # Base Intent
        is_action_intent = any(w in query_lower
                for w in ["what to do", "how", "fix", "resolve", "mitigate", "restart"]
        )


        is_cause_intent = any(
            w in query_lower
            for w in ["why", "cause", "happened", "root"]
        )



        is_log_intent = any(
            w in query_lower
            for w in ["log", "error", "meaning", "exit code", "crash"]
        )



        if any(s in section for s in high_value_sections):
            score += 4


        if any(s in section for s in low_value_sections):
            score -= 1

        # boosting the category
        if is_action_intent and category == "runbook":
            score += 3
            

        if is_cause_intent and category == "incident":
            score += 4
            

        if is_log_intent and category == "log_doc":
            score += 4

      
        if is_cause_intent and category in ["incident", "log_doc"]:
            score += 2



        if is_action_intent and category in ["incident"]:
            score += 1  

        scored_docs.append((score, doc))


    # sort by the score
    scored_docs.sort(key=lambda x: x[0], reverse=True)

    
    final_docs = []
    category_count = defaultdict(int)

    for score, doc in scored_docs:
        
        cat = doc.metadata.get("category")

        if category_count[cat] >= max_per_category:
            continue
        

        final_docs.append(doc)
        category_count[cat] += 1

        if len(final_docs) >= top_k:
            break

    return final_docs
