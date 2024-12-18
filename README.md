# Reliable RAG Agent

A Python-based RAG (Retrieval-Augmented Generation) system that processes PDF documents and provides accurate answers using local LLM models and vector store capabilities.

## Features

- PDF document processing with smart chunking
- Local LLM integration using Ollama (llama3.3:70b-instruct)
- Vector store implementation using Chroma
- Text cleaning and preprocessing
- Retrieval-based question answering
- Router system for query classification
- Document grading for response quality

## Prerequisites

- Python 3.12+
- Ollama installed with llama3.3:70b-instruct model
- Required Python packages (see requirements below)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd reliable_rag_agent
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install langchain langchain-community langchain-core python-dotenv chromadb pypdf langchain-nomic
```

4. Set up environment variables in `.env`:
```
TAVILY_API_KEY=your_tavily_key
LANGCHAIN_API_KEY=your_langchain_key
LANGCHAIN_TRACING_V2=false
LANGCHAIN_PROJECT=adaptive-rag
```

## Usage

1. Place your PDF document in the `storage` directory

2. Run the main script:
```bash
python src/rag_agent.py
```

3. The script will:
   - Process the PDF and create embeddings
   - Store vectors in a Chroma database
   - Allow querying the document using natural language
   - Provide relevant answers based on the document content

## Project Structure

```
reliable_rag_agent/
├── src/
│   ├── rag_agent.py    # Main RAG implementation
│   └── prompt.py       # Prompt templates
├── storage/
│   └── vectorstore/    # Chroma vector database
├── .env                # Environment variables
└── README.md
```

## Features in Detail

### Document Processing
- Smart text chunking with overlap
- Special character cleaning
- Table of contents removal
- Metadata preservation

### Vector Store
- Chroma-based vector database
- Persistent storage
- Efficient similarity search
- Configurable retrieval parameters

### LLM Integration
- Local Ollama model usage
- Zero-temperature for consistent outputs
- JSON mode support for structured outputs
- System and human message handling

## Contributing

Feel free to submit issues and enhancement requests!

## License

[Your chosen license] 