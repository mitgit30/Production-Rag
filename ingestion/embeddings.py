from langchain_community.embeddings import OllamaEmbeddings
# from dotenv import load_dotenv

def generate_embeddings():
    """
    generate the embeddings for future vector store search and retrieval functionality
    
    """
    embeddings=OllamaEmbeddings(
        model="nomic-embed-text",
        base_url="http://localhost:11434",
        
        
        
    )
    
    return embeddings