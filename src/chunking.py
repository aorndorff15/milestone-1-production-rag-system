from langchain.text_splitter import RecursiveCharacterTextSplitter

def create_chunks(documents, chunk_size=1000, chunk_overlap=100):
    """Split documents into overlapping chunks."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap)

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    return chunks