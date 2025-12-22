from ingestion.loader import load_data
from ingestion.metadata import extract_metadata


docs = load_data()
ex_met = extract_metadata(documents=docs)

for doc in ex_met[:1]:
    print(doc.metadata)

