
from typing import Optional
from retrieval.retriever import retrieve
from retrieval.reranker import rerank
from rag.prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from rag.guardrails import apply_guardrails, GuardrailViolation

from langchain_ollama.llms import OllamaLLM

# orchestration= retrieve --> rerank --> guardrails --> prompt --> LLM

def build_context(documents):
    context_blocks = []
    seen_sections = set()

    for doc in documents:
        section = (doc.metadata.get("section") or "").strip()

        # Deduplicate sections
        section_key = section.lower()
        if section_key in seen_sections:
            continue
        seen_sections.add(section_key)


        content = doc.page_content.strip()

        
        for marker in ["answer:", "following the above", "in summary"]:
            content = content.replace(marker, "")

        block = f"[{section}]\n{content}"
        context_blocks.append(block)

    return "\n\n".join(context_blocks)


def get_llm():
    """
    Initialize and return the LLM.
    
    """
    return OllamaLLM(
        model="gpt-oss:120b-cloud",
        temperature=0.2,
        
        
    )


def run_rag(query: str,category: Optional[str] = None,retrieve_k: int = 10,rerank_k: int = 5):
    """
    Run the full RAG pipeline for a user query.
    
    """

    # retrive
    retrieved_docs = retrieve(query=query,category=category,k=retrieve_k )

    
    # rerank
    reranked_docs = rerank(query=query,documents=retrieved_docs,top_k=rerank_k)

    # guardrails
    try:
        apply_guardrails(query, reranked_docs)
    except GuardrailViolation as e:
        return {
            "answer": str(e),
            "sources": [],
        }

    # construct the context
    context = build_context(reranked_docs)

    user_prompt = USER_PROMPT_TEMPLATE.format(
        question=query,
        context=context,
    )

    final_prompt = f"{SYSTEM_PROMPT}\n\n{user_prompt}"
    

    # call the llm
    llm = get_llm()
    final_answer = []


    for chunk in llm.stream(final_prompt):
        final_answer.append(chunk)

    answer = "".join(final_answer)

    return {
        "answer": answer.strip(),
        "sources": [
            {
                "source_file": doc.metadata.get("source_file"),
                "section": doc.metadata.get("section"),
                "category": doc.metadata.get("category"),
            }
            for doc in reranked_docs
        ],
    }
