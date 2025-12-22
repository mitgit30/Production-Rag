from retrieval.vector_store import get_vector_store

def retrieve(query:str,category:str | None , k :int = 5):
    """
    Retrieve relevant documents for a query.
    retrieve list of chunk documents by similarity search
    """
    vector_store = get_vector_store()
    
     # If no category is defined, do plain similarity search
    if category is None:
        docs = vector_store.similarity_search(query, k=k)
        return docs
    
     # Metadata based filtered retrieval
    docs = vector_store.similarity_search(query,k=k,filter={"category": category})
    
    return docs
