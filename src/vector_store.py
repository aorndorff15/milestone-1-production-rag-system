from langchain_community.vectorstores import Chroma


def create_vector_store(
    chunks,
    embeddings,
    embedding_model,
    collection_name="apollo_rag"):
    """Create a Chroma vector store using precomputed embeddings."""

    texts = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=embedding_model)

    vectorstore._collection.upsert(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings)

    return vectorstore