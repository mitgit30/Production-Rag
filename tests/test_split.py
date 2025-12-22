from ingestion.splitter import split_documents
from ingestion.loader import load_data


print("-"*50)
documents = load_data()
chunks = split_documents(documents=documents)
print(len(chunks))