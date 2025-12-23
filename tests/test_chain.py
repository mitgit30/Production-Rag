from rag.chain import run_rag

def run_chain():
    result = run_rag(query="Can we safely restart pods to resolve database connection exhaustion when logs show OOMKilled and this issue occurred before? What conditions must be verified first?")
    
    print(result["answer"])

    print("\nSources:\n")
    for s in result["sources"]:
        print(s)
        
run_chain()