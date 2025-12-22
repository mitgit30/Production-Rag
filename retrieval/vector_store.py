from langchain_community.vectorstores import FAISS
from ingestion.embeddings import generate_embeddings
from core.config import VECTOR_STORE_DIR
import os
_vector_store = None  # Global variable to store the vector store instance
def get_vector_store():
    """
    Loads and returns the FAISS vector store.
    Uses a singleton pattern to avoid reloading on every call.
    
    """
    global _vector_store
    if _vector_store is None:
        if not os.path.exists(VECTOR_STORE_DIR):
            raise RuntimeError("Vector store not found. Run ingestion before retrieval.")
        
        
    embeddings = generate_embeddings()
    _vector_store = FAISS.load_local(folder_path=VECTOR_STORE_DIR, embeddings=embeddings , allow_dangerous_deserialization=True,)
    return _vector_store