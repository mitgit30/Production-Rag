from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.query import router as query_router

app = FastAPI(
    title="Engineering Operations RAG Assistant",
     description="Production-grade RAG system for SRE / Platform / DevOps knowledge",
     
)

# Cors Safety

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=query_router, prefix="/query", tags=["query"])

@app.get("/")
def root():
    return {
        "service": "Engineering Operations RAG Assistant",
        "status": "running",
        "endpoints": ["/query"],
    }