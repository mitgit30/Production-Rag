from ingestion.loader import load_data

docs = load_data()

for doc in docs[:1]:
    print("Content:", doc.page_content[:500])