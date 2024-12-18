# Reliable RAG Agent

A Python-based RAG (Retrieval-Augmented Generation) system that processes PDF documents and provides accurate answers using local LLM models and vector store capabilities. The system includes advanced features like routing, document grading, and hallucination detection.

## Features

- PDF document processing with smart chunking and text cleaning
- Local LLM integration using Ollama (llama3.3:70b-instruct)
- Vector store implementation using Chroma and SKLearn
- Advanced text cleaning and preprocessing
- Multi-stage RAG pipeline:
  - Query routing (web search vs. document search)
  - Document relevance grading
  - Hallucination detection
  - Answer generation with context validation

## Prerequisites

- Python 3.12+
- Ollama installed with llama3.3:70b-instruct model
- Conda for environment management

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd reliable_rag_agent
```

2. Create and activate the conda environment:
```bash
conda env create -f environment.yml
conda activate adaptive_rag
```

3. Install additional requirements:
```bash
pip install -r requirements.txt
```

4. Set up environment variables in `.env`:
```
OPENAI_API_KEY=your_openai_key
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
   - Process the PDF with smart chunking
   - Clean and preprocess the text
   - Create and store embeddings
   - Enable intelligent query routing
   - Grade document relevance
   - Check for hallucinations
   - Provide accurate answers based on the document content

## Project Structure

```
reliable_rag_agent/
├── src/
│   ├── rag_agent.py    # Main RAG implementation
│   └── prompt.py       # Prompt templates and instructions
├── storage/
│   └── vectorstore/    # Vector database storage
├── environment.yml     # Conda environment specification
├── requirements.txt    # Python package requirements
├── .env               # Environment variables
└── README.md
```

## Features in Detail

### Document Processing
- Smart text chunking with configurable overlap
- Advanced text cleaning:
  - Special character removal
  - Page number cleaning
  - Table of contents filtering
  - Whitespace normalization
- Metadata preservation

### Vector Store
- Multiple vector store options (Chroma, SKLearn)
- Persistent storage
- Configurable similarity search
- Efficient retrieval parameters

### LLM Integration
- Local Ollama model usage
- Zero-temperature for consistent outputs
- JSON mode for structured outputs
- System and human message handling

### Advanced RAG Features
- Query routing between web search and document search
- Document relevance grading
- Hallucination detection
- Context-aware answer generation
- Multi-stage validation pipeline

## Environment Management

The project uses a conda environment named `adaptive_rag` with Python 3.12. Key dependencies include:
- langchain and its ecosystem (community, core, nomic)
- Local embedding models via nomic
- Local LLMs via Ollama
- Vector stores (Chroma, SKLearn)
- Web search capabilities via Tavily

## Contributing

Feel free to submit issues and enhancement requests!

## License

[MIT License] 