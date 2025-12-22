from retrieval.vector_store import get_vector_store

def main():
    db = get_vector_store()
    print("Vector store loaded successfully")
    print("Index size:", db.index.ntotal)

if __name__ == "__main__":
    main()