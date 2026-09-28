from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


def load_documents(folder_path):
    """Load all PDF documents from a folder."""

    documents = []

    # Load PDF documents from folder into documents
    for pdf_path in Path(folder_path).glob("*.pdf"):
        loader = PyPDFLoader(str(pdf_path))
        documents.extend(loader.load())

    print(f"Loaded {len(documents)} total pages")
    print(f"Found {len(set(doc.metadata['source'] for doc in documents))} documents")

    if documents:
        print(documents[0].page_content[:500] + "...")

    return documents
