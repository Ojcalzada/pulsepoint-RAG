import streamlit as st
from rag_engine import initialize_rag_chain, query_rag, check_safety_guardrails
import time

# Page configuration with modern styling
st.set_page_config(
    page_title="PulsePoint | Healthcare Consensus Engine",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS with 2026 design trends
st.markdown("""
    <style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Modern header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.15);
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .main-subtitle {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.9);
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* Search container */
    .search-container {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
        margin-bottom: 2rem;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        padding: 0.875rem 1rem;
        font-size: 1rem;
        transition: all 0.2s ease;
        background: #fafafa;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        background: white;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        border: none;
        transition: all 0.2s ease;
        letter-spacing: 0.01em;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        transform: translateY(-1px);
    }
    
    .stButton > button[kind="secondary"] {
        background: white;
        color: #374151;
        border: 2px solid #e5e7eb;
    }
    
    .stButton > button[kind="secondary"]:hover {
        border-color: #667eea;
        color: #667eea;
    }
    
    /* Alert boxes */
    .alert-box {
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin: 1.5rem 0;
        border-left: 4px solid;
        display: flex;
        align-items: start;
        gap: 1rem;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left-color: #f59e0b;
        color: #78350f;
    }
    
    .alert-error {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left-color: #ef4444;
        color: #7f1d1d;
    }
    
    .alert-info {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left-color: #3b82f6;
        color: #1e3a8a;
    }
    
    .alert-icon {
        font-size: 1.5rem;
        line-height: 1;
    }
    
    /* Answer card */
    .answer-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(0, 0, 0, 0.05);
        position: relative;
        overflow: hidden;
    }
    
    .answer-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .question-label {
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .question-text {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 1.5rem;
        line-height: 1.5;
    }
    
    .answer-text {
        font-size: 1rem;
        line-height: 1.75;
        color: #374151;
    }
    
    /* Source card */
    .source-card {
        background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        border: 1px solid #e5e7eb;
    }
    
    .source-title {
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #6b7280;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .source-list {
        font-size: 0.9375rem;
        color: #4b5563;
        line-height: 1.8;
    }
    
    /* Example cards */
    .example-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .example-card {
        background: white;
        border-radius: 12px;
        padding: 1.25rem;
        border: 2px solid #e5e7eb;
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: left;
    }
    
    .example-card:hover {
        border-color: #667eea;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.15);
        transform: translateY(-2px);
    }
    
    .example-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    .example-text {
        font-size: 0.9375rem;
        color: #374151;
        line-height: 1.5;
        font-weight: 500;
    }
    
    /* Stats bar */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        flex: 1;
        min-width: 200px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        line-height: 1;
    }
    
    .stat-label {
        font-size: 0.875rem;
        color: #6b7280;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #f9fafb;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f9fafb 0%, #ffffff 100%);
        border-right: 1px solid #e5e7eb;
    }
    
    /* History items */
    .history-item {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        border: 1px solid #e5e7eb;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .history-item:hover {
        border-color: #667eea;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
    }
    
    /* Loading animation */
    .loading-container {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1.5rem;
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: white;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        font-weight: 500;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #667eea;
    }
    
    /* Spacing utilities */
    .spacer-sm { margin: 1rem 0; }
    .spacer-md { margin: 2rem 0; }
    .spacer-lg { margin: 3rem 0; }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-title { font-size: 2rem; }
        .stat-card { min-width: 100%; }
        .example-grid { grid-template-columns: 1fr; }
    }
    </style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'qa_chain' not in st.session_state:
        st.session_state.qa_chain = None
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'system_ready' not in st.session_state:
        st.session_state.system_ready = False

def display_header():
    """Display modern header."""
    st.markdown("""
        <div class="main-header">
            <div class="main-title">PulsePoint</div>
            <div class="main-subtitle">AI-Powered Healthcare Consensus Engine</div>
        </div>
    """, unsafe_allow_html=True)

def display_medical_disclaimer():
    """Display medical disclaimer alert."""
    st.markdown("""
        <div class="alert-box alert-warning">
            <div class="alert-icon">⚕️</div>
            <div>
                <strong>Medical Disclaimer</strong><br>
                This system provides summaries of peer experiences from health communities.
                It is NOT a substitute for professional medical advice, diagnosis, or treatment.
                Always consult qualified healthcare providers for medical decisions.
            </div>
        </div>
    """, unsafe_allow_html=True)

def load_rag_system():
    """Load RAG system with progress indicator."""
    if not st.session_state.system_ready:
        with st.spinner("Initializing PulsePoint engine..."):
            try:
                st.session_state.qa_chain = initialize_rag_chain()
                st.session_state.system_ready = True
            except Exception as e:
                st.error(f"❌ Failed to initialize system: {e}")
                st.stop()

def display_stats():
    """Display system statistics."""
    st.markdown("""
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-value">80+</div>
                <div class="stat-label">Health Discussions</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">360+</div>
                <div class="stat-label">Peer Experiences</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">12+</div>
                <div class="stat-label">Conditions Covered</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def display_search_interface():
    """Display modern search interface."""
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    st.markdown("### Search Health Experiences")
    st.markdown("Ask about symptoms, treatments, or lifestyle strategies")
    
    query = st.text_input(
        "Your question",
        placeholder="e.g., What has helped people manage chronic migraines?",
        label_visibility="collapsed",
        key="search_input"
    )
    
    col1, col2, col3 = st.columns([2, 2, 3])
    
    with col1:
        search_button = st.button("🔍 Search", type="primary", use_container_width=True)
    
    with col2:
        clear_button = st.button("🗑️ Clear History", type="secondary", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if clear_button:
        st.session_state.history = []
        st.rerun()
    
    return query, search_button

def display_example_queries():
    """Display example query cards."""
    st.markdown("### Try These Examples")
    
    examples = [
        {"icon": "🧠", "text": "What has helped people with chronic migraines?"},
        {"icon": "⚡", "text": "How do people manage fibromyalgia pain?"},
        {"icon": "💤", "text": "What natural approaches improve sleep quality?"},
        {"icon": "🌫️", "text": "Strategies for dealing with brain fog?"},
        {"icon": "😰", "text": "How to manage anxiety symptoms naturally?"},
        {"icon": "🦴", "text": "What helps with arthritis pain?"}
    ]
    
    # Create grid of example cards
    cols = st.columns(3)
    for idx, example in enumerate(examples):
        with cols[idx % 3]:
            if st.button(
                f"{example['icon']} {example['text']}", 
                key=f"example_{idx}",
                use_container_width=True
            ):
                return example['text']
    
    return None

def display_answer_card(query, answer, sources):
    """Display answer with modern card design."""
    st.markdown('<div class="answer-card">', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="question-label">Your Question</div>
        <div class="question-text">{query}</div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="answer-text">{answer}</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="source-card">
            <div class="source-title">
                <span>📚</span>
                <span>Sources Referenced</span>
            </div>
            <div class="source-list">{sources.replace(chr(10), '<br>')}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_safety_alert(message):
    """Display safety alert."""
    st.markdown(f"""
        <div class="alert-box alert-error">
            <div class="alert-icon">🚨</div>
            <div>{message.replace(chr(10), '<br>')}</div>
        </div>
    """, unsafe_allow_html=True)

def display_sidebar():
    """Display modern sidebar."""
    with st.sidebar:
        st.markdown("### 📊 Session Info")
        
        # System status
        if st.session_state.system_ready:
            st.success("✅ System Ready")
        else:
            st.info("⏳ Initializing...")
        
        st.markdown("---")
        
        # Query count
        query_count = len(st.session_state.history)
        st.metric("Queries This Session", query_count)
        
        if query_count > 0:
            st.markdown("---")
            st.markdown("### 📜 Recent Queries")
            
            # Display recent queries (last 5)
            for idx, item in enumerate(reversed(st.session_state.history[-5:])):
                with st.expander(f"Query {query_count - idx}"):
                    st.markdown(f"**Q:** {item['query'][:80]}...")
                    st.markdown(f"**A:** {item['answer'][:150]}...")
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
            **PulsePoint** aggregates peer health experiences to provide 
            consensus insights on wellness strategies.
            
            - 🔒 Privacy-first design
            - 📚 Source citations
            - ⚕️ Medical disclaimers
            - 🛡️ Safety guardrails
        """)
        
        st.markdown("---")
        st.markdown("""
            <div style="text-align: center; color: #6b7280; font-size: 0.875rem;">
                Built with Python, LangChain,<br>ChromaDB & Groq
            </div>
        """, unsafe_allow_html=True)

def main():
    """Main application logic."""
    initialize_session_state()
    display_header()
    display_medical_disclaimer()
    
    # Load system
    load_rag_system()
    
    # Display stats
    display_stats()
    
    # Sidebar
    display_sidebar()
    
    # Main content area
    query, search_button = display_search_interface()
    
    # Example queries
    example_query = display_example_queries()
    if example_query:
        query = example_query
        search_button = True
    
    # Process query
    if search_button and query:
        # Safety check
        is_safe, safety_message = check_safety_guardrails(query)
        
        if not is_safe:
            display_safety_alert(safety_message)
        else:
            # Show loading state
            with st.spinner("🔍 Searching peer experiences..."):
                try:
                    answer, sources = query_rag(st.session_state.qa_chain, query)
                    
                    # Add to history
                    st.session_state.history.append({
                        'query': query,
                        'answer': answer,
                        'sources': sources
                    })
                    
                    # Display result
                    display_answer_card(query, answer, sources)
                    
                except Exception as e:
                    st.error(f"❌ Error processing query: {e}")
    
    elif search_button and not query:
        st.warning("⚠️ Please enter a question")
    
    # Display history
    if len(st.session_state.history) > 1:
        st.markdown("---")
        st.markdown("### 📚 Previous Questions")
        
        # Show all but the most recent (which is already displayed)
        for idx, item in enumerate(reversed(st.session_state.history[:-1])):
            with st.expander(f"Question {len(st.session_state.history) - idx - 1}: {item['query'][:60]}..."):
                display_answer_card(item['query'], item['answer'], item['sources'])

if __name__ == "__main__":
    main()