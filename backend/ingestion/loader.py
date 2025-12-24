from langchain_community.document_loaders import DirectoryLoader , TextLoader
from core.config import DATA_DIR
import os

def load_data():
    """
    Load the data from respective respositories and return the particular documents
    """
    files = []
    folders = ["runbooks","incidents","infra_docs","logs"]
    
    for folder in folders:
        folder_path = os.path.join(DATA_DIR, folder)
        
        if not os.path.exists(folder_path):
            continue
        
        loader = DirectoryLoader(folder_path ,glob="**/*.md",loader_cls=TextLoader,show_progress=True,loader_kwargs={"encoding": "utf-8"})
        
        docs = loader.load()
        files.extend(docs)
        
    return files
    