from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from typing import Optional

from rag.chain import run_rag

router = APIRouter()

# pydantic schema
class Query(BaseModel):
    question : str
    # category : Optional[str] = None # Category is optional
    
    
# Query Endpoint
@router.post("/") # query router
def rag_query(query:Query):
    
    if not query.question.strip():
        raise HTTPException(status_code=400, detail="Query is required")
    
    try:
        result = run_rag(query=query.question)
        return {
         "answer":result["answer"],
           "sources" : result["sources"],
            
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
