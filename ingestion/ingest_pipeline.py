from ingestion.loader import load_data
from ingestion.splitter import split_documents
from ingestion.metadata import extract_metadata
from ingestion.embeddings import generate_embeddings
from langchain_community.vectorstores import FAISS
from core.config import VECTOR_STORE_DIR
import os

    
## First build the vectors
    
def build_vectors(chunks):
    embeddings = generate_embeddings()
    vector_store = FAISS.from_documents(documents=chunks,embedding=embeddings)
    vector_store.save_local(VECTOR_STORE_DIR)
        
        
 # Now implement ingestion pipeline
    
def run_ingestion():
        
    documents = load_data() # Loading the files and documents
    documents = extract_metadata(documents=documents) # extracting the metadata from particular files/documents
    chunks = split_documents(documents)  # splitting the documents into smaller chunks using smart chunking techniques
    build_vectors(chunks) # building the vector store db
        
    print("Ingestion pipeline implemented successfully")
    print(f"Total documents loaded : {len(documents)}")
    print(f"Total chunks created : {len(chunks)}")
    print(f"Vector store saved at : {VECTOR_STORE_DIR} (in root directory)")


run_ingestion() # trigger the ingestion
        