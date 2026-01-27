import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# Configuration
CHROMA_DB_PATH = "./chroma_db"
GROQ_MODEL = "llama-3.3-70b-versatile"
RETRIEVAL_K = 4

# Safety keywords that trigger medical disclaimer
HIGH_RISK_KEYWORDS = [
    "suicide", "kill myself", "end my life", "self-harm", "cut myself",
    "emergency", "chest pain", "can't breathe", "heart attack", "stroke",
    "surgery", "operate", "prescribe", "diagnosis", "blood", "severe pain"
]

def get_api_key():
    """
    Get API key from Streamlit secrets (cloud) or environment variable (local).
    Works seamlessly in both development and production.
    """
    # Try Streamlit secrets first (for Streamlit Cloud deployment)
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and 'GROQ_API_KEY' in st.secrets:
            return st.secrets['GROQ_API_KEY']
    except ImportError:
        # Streamlit not installed (running standalone)
        pass
    except Exception:
        # Streamlit secrets not configured yet
        pass
    
    # Fallback to environment variable (for local .env)
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found!\n\n"
            "For local development:\n"
            "  1. Create .streamlit/secrets.toml\n"
            "  2. Add: GROQ_API_KEY = 'your_key_here'\n\n"
            "For Streamlit Cloud:\n"
            "  1. Go to app settings\n"
            "  2. Add secret: GROQ_API_KEY = 'your_key_here'"
        )
    
    return api_key

def check_safety_guardrails(query):
    """
    Check if the query contains high-risk keywords that require
    immediate professional intervention.
    
    Args:
        query: User's search query
        
    Returns:
        Tuple of (is_safe, safety_message)
    """
    query_lower = query.lower()
    
    for keyword in HIGH_RISK_KEYWORDS:
        if keyword in query_lower:
            safety_message = (
                "Your query suggests you may need immediate professional medical assistance. "
                "Please contact:\n\n"
                "- Emergency Services: 911 (US) or your local emergency number\n"
                "- National Suicide Prevention Lifeline: 988 (US)\n"
                "- Crisis Text Line: Text HOME to 741741\n\n"
                "This system provides peer experiences only and is NOT a substitute for "
                "professional medical care."
            )
            return False, safety_message
    
    return True, None

def initialize_rag_chain():
    """
    Initialize the RAG chain with ChromaDB retriever and Groq LLM.
    
    Returns:
        Configured RetrievalQA chain
    """
    # Get API key using universal method
    api_key = get_api_key()
    
    print("Loading vector store...")
    # Initialize the same embeddings model used during ingestion
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    # Load the persisted ChromaDB
    vectorstore = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings
    )
    
    # Create retriever that fetches top K relevant chunks
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": RETRIEVAL_K}
    )
    
    print("Initializing Groq LLM...")
    # Initialize Groq with Llama 3.3 70B
    llm = ChatGroq(
        model=GROQ_MODEL,
        temperature=0.3,
        max_tokens=1024,
        groq_api_key=api_key  # Pass key explicitly
    )
    
    # Custom prompt template with medical disclaimer
    prompt_template = """You are a helpful assistant that summarizes peer experiences from healthcare communities on Reddit. Your role is to synthesize what others have shared about their personal health journeys.

CRITICAL INSTRUCTIONS:
1. Base your answer ONLY on the context provided below
2. If the answer is not in the context, say "I don't have information about that in the available peer experiences"
3. Always cite which thread the information came from using the thread_id
4. Never provide medical diagnoses or treatment recommendations
5. Always end with: "IMPORTANT: This information represents peer experiences only and is NOT medical advice. Please consult a healthcare professional for medical guidance."

Context from peer discussions:
{context}

Question: {question}

Answer:"""

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    # Create the RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )
    
    print("RAG engine initialized successfully\n")
    return qa_chain

def format_sources(source_documents):
    """
    Format source documents into readable citations.
    
    Args:
        source_documents: List of retrieved Document objects
        
    Returns:
        Formatted string with source citations
    """
    if not source_documents:
        return "No sources available"
    
    sources = []
    seen_threads = set()
    
    for doc in source_documents:
        thread_id = doc.metadata.get('thread_id', 'unknown')
        if thread_id not in seen_threads:
            source = doc.metadata.get('source', 'Unknown source')
            title = doc.metadata.get('title', 'Untitled')
            sources.append(f"- {source}: {title}")
            seen_threads.add(thread_id)
    
    return "\n".join(sources)

def query_rag(qa_chain, question):
    """
    Query the RAG system with safety checks and source citation.
    
    Args:
        qa_chain: Initialized RetrievalQA chain
        question: User's health query
        
    Returns:
        Tuple of (answer, sources)
    """
    # Safety check
    is_safe, safety_message = check_safety_guardrails(question)
    if not is_safe:
        return safety_message, "Safety guardrail triggered - no sources consulted"
    
    # Execute RAG query
    print(f"Querying: {question}")
    print("Retrieving relevant peer experiences...\n")
    
    result = qa_chain.invoke({"query": question})
    
    answer = result['result']
    sources = format_sources(result['source_documents'])
    
    return answer, sources

def main():
    """
    Main function for testing the RAG engine with sample queries.
    """
    print("=" * 60)
    print("PulsePoint RAG Engine - Testing Mode")
    print("=" * 60)
    print()
    
    # Initialize the RAG chain
    try:
        qa_chain = initialize_rag_chain()
    except Exception as e:
        print(f"ERROR: Failed to initialize RAG engine: {e}")
        return
    
    # Test queries
    test_queries = [
        "What has helped people with chronic lower back pain?",
        "How do people manage fatigue with hypothyroidism?",
        "What are some strategies for dealing with brain fog?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'=' * 60}")
        print(f"Test Query {i}")
        print(f"{'=' * 60}")
        
        answer, sources = query_rag(qa_chain, query)
        
        print(f"\nAnswer:\n{answer}")
        print(f"\nSources:\n{sources}")
    
    print(f"\n{'=' * 60}")
    print("Testing complete. The RAG engine is ready for use.")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    main()