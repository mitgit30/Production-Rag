
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter


def split_documents(documents):
    """
    split the documents into smaller chunks based on markdown headers and size constraints.
    
    """
    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("##", "section"),
        ]
    )

    header_chunks = []
    for doc in documents:
        splits = header_splitter.split_text(doc.page_content)
        for s in splits:
            s.metadata.update(doc.metadata)
        header_chunks.extend(splits)

    
    size_splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
        separators=["\n\n", "\n", " "],
    )

    chunks = size_splitter.split_documents(header_chunks)
    return chunks
