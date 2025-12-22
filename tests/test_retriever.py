from retrieval.retriever import retrieve

def test_retriever():
    docs = retrieve( query="what to do when connection gest exhaust", k=5,category="runbook" )

    for d in docs:
        print(d.metadata.get("source_file"))
        print(d.metadata.get("section"))
        print(d.page_content[:600])
        

if __name__ == "__main__":    
    test_retriever()