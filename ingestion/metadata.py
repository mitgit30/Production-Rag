
import os

def extract_metadata(documents):
    """"
    Extracts metadata from the particular documents based on file properties.
    
    """
    
    for doc in documents:
        file_path = doc.metadata.get("file_path", "")
        
        normalized_path = file_path.replace("\\", "/") # Normalize path for cross-platform compatibility
        
        # Determining category from folder names
        
        if "/runbooks/" in normalized_path:
            category = "runbook"
            
        elif "/incidents/" in normalized_path:
            category = "incident"
            
        elif "/infra_docs/" in normalized_path:
            category = "infra_doc"
            
        elif "/logs/" in normalized_path:
            category = "log_doc"
            
        else:
            category = "unknown"
            
        
        # Determine the domain and set other metadata fields
            
        doc.metadata["category"] = category
        doc.metadata["domain"] = "sre"
        doc.metadata["source_file"] = os.path.basename(normalized_path)
        doc.metadata["source_path"] = normalized_path
        
    
    return documents