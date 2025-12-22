from rag.chain import run_rag

def run_chain():
    result = run_rag(query="After a CI/CD deployment, the service has partial availability and increased 5xx errors. Logs show CrashLoopBackOff. How should this be diagnosed, what was the likely root cause in past incidents, and what rollback approach is safest?")
    
    print(result["answer"])

    print("\nSOURCES:\n")
    for s in result["sources"]:
        print(s)
        
run_chain()