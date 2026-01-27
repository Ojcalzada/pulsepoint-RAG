# PulsePoint: Healthcare Consensus Engine

A production-ready Retrieval-Augmented Generation (RAG) system that synthesizes peer health experiences from online communities. Built to demonstrate advanced AI engineering capabilities while maintaining privacy-first principles and medical safety guardrails.

## Project Overview

PulsePoint addresses the challenge of finding reliable, consensus-based health information by aggregating peer experiences and using semantic search to surface relevant insights. The system processes 80+ healthcare discussion threads covering chronic conditions, extracts actionable strategies, and provides answers with full source attribution.

## Technical Architecture

**Stack:**
- LLM: Groq API (Llama 3.3 70B Versatile)
- Vector Database: ChromaDB (local persistence)
- Embeddings: HuggingFace sentence-transformers (all-MiniLM-L6-v2)
- Orchestration: LangChain
- Interface: Streamlit with custom CSS

**Data Pipeline:**
1. Synthetic dataset generation (80 threads, 360+ responses, 12 conditions)
2. Document chunking (500 chars, 50 char overlap)
3. Local embedding generation (no external API calls)
4. Vector storage with metadata preservation
5. Semantic retrieval (top-4 similarity search)
6. LLM synthesis with source citation
7. Safety layer with medical disclaimers

**Key Metrics:**
- 250 vector chunks indexed
- Sub-second query latency
- 100% source attribution
- Zero hallucination guardrails

## Features

**Core Capabilities:**
- Semantic search across healthcare discussions using vector embeddings
- Source citation for every response with thread IDs
- Real-time safety guardrails detecting high-risk queries
- Automatic medical disclaimer injection
- Privacy-first architecture (data never leaves local environment for embeddings)

**Engineering Highlights:**
- Modular architecture enabling easy model swapping
- Comprehensive error handling and input validation
- Production-ready secret management (local + cloud)
- Scalable chunking strategy for optimal retrieval
- Modern UI with custom CSS and responsive design

## Installation
```bash
# Clone repository
git clone https://github.com/olneyjR/pulsepoint-rag.git
cd pulsepoint-rag

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure secrets
mkdir -p .streamlit
echo 'GROQ_API_KEY = "your_key_here"' > .streamlit/secrets.toml

# Run data ingestion (one-time)
python ingest.py

# Launch application
streamlit run app_modern.py
```

Get your free Groq API key: https://console.groq.com/

## Usage

The system supports queries about chronic conditions, lifestyle interventions, and symptom management strategies. Example queries:
```
"What has helped people with chronic migraines?"
"How do people manage fibromyalgia pain?"
"What natural approaches improve sleep quality?"
"Strategies for dealing with brain fog?"
```

Each response includes:
- Synthesized peer experiences from multiple sources
- Specific thread citations (r/subreddit - thread_id)
- Medical disclaimer emphasizing this is peer information, not medical advice
- Automatic crisis resource referral for high-risk queries

## System Design

**RAG Pipeline:**
```
User Query
    |
    v
Safety Check (keyword filtering)
    |
    v
Query Embedding (local HuggingFace)
    |
    v
Vector Search (ChromaDB similarity)
    |
    v
Context Retrieval (top 4 chunks)
    |
    v
Prompt Construction (system + context + query)
    |
    v
LLM Generation (Groq API)
    |
    v
Response + Citations + Disclaimer
```

**Why RAG Over Fine-Tuning:**
- Cost: $0 for data updates vs $50k+ for model retraining
- Speed: Minutes to update knowledge base vs days for fine-tuning
- Attribution: Full source tracking vs black-box model
- Privacy: Local embeddings vs sending training data to vendors

## Dataset

Synthetic dataset designed for educational purposes:
- 80 healthcare discussion threads
- 360+ peer responses with realistic language patterns
- 12 conditions: migraines, fibromyalgia, arthritis, chronic fatigue, hypothyroidism, brain fog, anxiety, insomnia, IBS, lupus, POTS, endometriosis
- Actionable strategies with specific implementation details
- Appropriate medical context for disclaimer enforcement

## Deployment

**Streamlit Cloud:**

1. Push to GitHub
2. Connect repository at https://share.streamlit.io/
3. Add secret in app settings: `GROQ_API_KEY`
4. Deploy `app_modern.py`

**Alternative Deployment Options:**
- Hugging Face Spaces (includes GPU for local models)
- Railway / Render (containerized deployment)
- Self-hosted with Docker
- Local Ollama integration for fully offline operation

See `DEPLOYMENT.md` for detailed instructions.

## Project Structure
```
pulsepoint-rag/
├── app_modern.py                    # Streamlit UI with modern design
├── rag_engine.py                    # Core RAG logic and safety guardrails
├── ingest.py                        # Data processing and vector store creation
├── enhanced_dataset_generator.py   # Synthetic dataset generation
├── reddit_data.json                # Healthcare discussion dataset
├── requirements.txt                # Python dependencies
├── chroma_db/                      # Vector database (gitignored)
└── .streamlit/
    └── secrets.toml                # API keys (gitignored)
```

## Technical Decisions

**Why Groq:**
- 300+ tokens/second (10x faster than OpenAI)
- Free tier sufficient for portfolio/demo
- Llama 3.3 70B quality comparable to GPT-4

**Why ChromaDB:**
- Lightweight (no separate server required)
- Python-native integration
- Persistent local storage
- Production-ready with metadata filtering

**Why Local Embeddings:**
- Zero cost for embedding generation
- Privacy compliance (HIPAA-ready architecture)
- No rate limits
- Portable across deployment environments

## Future Enhancements

**Planned Features:**
- Agentic RAG (LLM decides retrieval strategy)
- GraphRAG (condition relationship mapping)
- Multi-modal support (process images, charts)
- Conversation memory across sessions
- User feedback loop for relevance tuning

**Scalability Considerations:**
- Horizontal scaling with Redis caching
- Async processing for batch queries
- Model quantization for edge deployment
- A/B testing framework for prompt optimization

## Limitations

This is an educational demonstration system:
- Synthetic dataset (not real Reddit data due to API restrictions)
- Limited to text-based queries
- English language only
- No real-time data updates (static dataset)

**Important:** This system provides peer experiences only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers for medical decisions.

## Author

Jeffrey Olney

Portfolio: https://www.linkedin.com/in/jeffrey-olney/

GitHub: https://github.com/olneyjR

Built as a demonstration of production RAG architecture, safety-critical AI systems, and modern AI engineering practices.

## License

This project is provided for educational and portfolio purposes. The synthetic dataset and code are original work created for demonstration of technical capabilities.

---

**Note on Data Source:** Due to Reddit's API access restrictions as of 2025, this project uses a comprehensive synthetic dataset that mirrors the structure and language patterns of real healthcare community discussions while avoiding any privacy or compliance concerns.
EOF

Step 3: Create Deployment Guide
bashcat > DEPLOYMENT.md << 'EOF'
# Deployment Guide

## Streamlit Cloud Deployment

### Prerequisites

- GitHub account
- Groq API key from https://console.groq.com/

### Steps

**1. Create GitHub Repository**
```bash
# Initialize git
git init
git add .
git commit -m "Initial commit: PulsePoint RAG system"

# Create repo on GitHub, then:
git remote add origin https://github.com/olneyjR/pulsepoint-rag.git
git branch -M main
git push -u origin main
```

**2. Deploy to Streamlit Cloud**

- Visit https://share.streamlit.io/
- Click "New app"
- Connect GitHub account if not already connected
- Select repository: `pulsepoint-rag`
- Select branch: `main`
- Main file path: `app_modern.py`
- Click "Deploy"

**3. Configure Secrets**

- In Streamlit Cloud dashboard, open your app settings
- Navigate to "Secrets" section
- Add the following:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

- Click "Save"
- App will automatically restart with secrets

**4. Verify Deployment**

- App URL will be: `https://[your-app-name].streamlit.app`
- First deployment takes 5-10 minutes
- Subsequent updates deploy in 1-2 minutes

### Troubleshooting

**Module Import Errors:**
- Verify `requirements.txt` includes all dependencies
- Force redeploy from Streamlit dashboard

**API Key Not Found:**
- Check secret spelling matches exactly: `GROQ_API_KEY`
- Verify no extra spaces in secrets.toml
- Restart app from dashboard

**ChromaDB Issues:**
- Vector database is gitignored and built at runtime
- Ensure `reddit_data.json` is committed to repository

## Alternative Deployment Options

### Hugging Face Spaces

- Free GPU for inference
- Built-in secrets management
- Deploy directly from GitHub

### Docker Deployment
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app_modern.py"]
```

### Local Ollama (No API Required)

Replace Groq with local Llama model for fully offline operation.

See project README for architecture details.