from langchain_openai import OpenAIEmbeddings


def create_embeddings(model="text-embedding-3-small"):
    """Create an embedding model using UNC AI Gateway"""

    embeddings = OpenAIEmbeddings(
        model=model)

    return embeddings

def embed_chunks(chunks, embedding_model, batch_size=200):
    """Create embeddings for document chunks in smaller batches"""

    texts = [chunk.page_content for chunk in chunks]

    embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_embeddings = embedding_model.embed_documents(batch, chunk_size=500)       
        embeddings.extend(batch_embeddings)

    return embeddings