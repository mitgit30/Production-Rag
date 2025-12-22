
from typing import List
from langchain_core.documents import Document


class GuardrailViolation(Exception):
    """Raised when guardrail checks fail.
    """
    pass


def validate_context(query: str,documents: List[Document],min_docs: int = 1):
    """
    Validate retrieved context before passing to LLM.
    """

    if not documents or len(documents) < min_docs:
        raise GuardrailViolation(
            "Insufficient context retrieved to answer the question.")

    return True


def check_domain_alignment(documents: List[Document],allowed_domains: List[str] = ["sre"]):
    """
    Ensure retrieved documents belong to expected domains.
    
    """

    for doc in documents:
        domain = doc.metadata.get("domain")
        if domain not in allowed_domains:
            raise GuardrailViolation(
                f"Document from unsupported domain detected: {domain}")

    return True


def prevent_unsafe_actions(query: str,documents: List[Document]):
    """
    Prevent generating unsafe operational guidance when context is weak.
    """

    risky_keywords = ["delete","drop","shutdown","terminate","wipe","format"]

    query_lower = query.lower()

    if any(word in query_lower for word in risky_keywords):
        has_runbook = any(
            doc.metadata.get("category") == "runbook"
            for doc in documents
        )

        if not has_runbook:
            raise GuardrailViolation(
                "Potentially destructive action requested without runbook context."
            )

    return True


def apply_guardrails(
    query: str,
    documents: List[Document],
):
    """
    Run all guardrail checks.
    """

    validate_context(query, documents)
    check_domain_alignment(documents)
    prevent_unsafe_actions(query, documents)

    return documents
