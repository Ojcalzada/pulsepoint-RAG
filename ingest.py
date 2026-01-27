import json
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document

# Configuration
CHROMA_DB_PATH = "./chroma_db"
MOCK_DATA_FILE = "reddit_data.json"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

def load_reddit_data(file_path):
    """
    Load Reddit thread data from JSON file.
    
    Args:
        file_path: Path to the mock_data.json file
        
    Returns:
        List of thread dictionaries
    """
    print(f"Loading data from {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Loaded {len(data['threads'])} threads")
    return data['threads']

def prepare_documents(threads):
    """
    Convert Reddit threads into LangChain Document objects.
    Each thread and its comments are combined into structured text.
    
    Args:
        threads: List of thread dictionaries
        
    Returns:
        List of Document objects with metadata
    """
    documents = []
    
    for thread in threads:
        # Combine the original post with all comments
        full_text = f"Thread Title: {thread['title']}\n\n"
        full_text += f"Original Post: {thread['post_text']}\n\n"
        full_text += "Community Responses:\n\n"
        
        for idx, comment in enumerate(thread['comments'], 1):
            full_text += f"Response {idx}: {comment['text']}\n\n"
        
        # Create document with metadata for citation tracking
        doc = Document(
            page_content=full_text,
            metadata={
                "thread_id": thread['thread_id'],
                "subreddit": thread['subreddit'],
                "title": thread['title'],
                "source": f"r/{thread['subreddit']} - {thread['thread_id']}"
            }
        )
        documents.append(doc)
    
    print(f"Prepared {len(documents)} documents for processing")
    return documents

def chunk_documents(documents):
    """
    Split documents into smaller chunks for better retrieval accuracy.
    Uses RecursiveCharacterTextSplitter to maintain context.
    
    Args:
        documents: List of Document objects
        
    Returns:
        List of chunked Document objects
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")
    return chunks

def create_vector_store(chunks):
    """
    Create a local ChromaDB vector store using HuggingFace embeddings.
    This runs entirely locally without external API calls.
    
    Args:
        chunks: List of chunked Document objects
        
    Returns:
        Chroma vector store object
    """
    print("Initializing local embeddings model...")
    # Use a small, efficient model that runs locally
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    print("Creating vector store...")
    # Create persistent ChromaDB store
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH
    )
    
    print(f"Vector store created at {CHROMA_DB_PATH}")
    return vectorstore

def main():
    """
    Main ingestion pipeline:
    1. Load Reddit JSON data
    2. Prepare documents with metadata
    3. Chunk documents for optimal retrieval
    4. Generate embeddings and store in ChromaDB
    """
    print("=" * 60)
    print("PulsePoint Data Ingestion Pipeline")
    print("=" * 60)
    
    # Check if mock data file exists
    if not os.path.exists(MOCK_DATA_FILE):
        print(f"ERROR: {MOCK_DATA_FILE} not found!")
        print("Please ensure mock_data.json is in the same directory.")
        return
    
    # Load and process data
    threads = load_reddit_data(MOCK_DATA_FILE)
    documents = prepare_documents(threads)
    chunks = chunk_documents(documents)
    
    # Create vector store
    vectorstore = create_vector_store(chunks)
    
    print("\n" + "=" * 60)
    print("Ingestion Complete!")
    print("=" * 60)
    print(f"Total chunks stored: {len(chunks)}")
    print(f"Vector DB location: {CHROMA_DB_PATH}")
    print("\nYou can now run the RAG engine to query this data.")

if __name__ == "__main__":
    main()