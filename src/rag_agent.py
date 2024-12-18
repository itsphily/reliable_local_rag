# Imports
#------------------------------------------------------------------------------
import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_nomic.embeddings import NomicEmbeddings
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_ollama import ChatOllama
import json
from langchain_core.messages import HumanMessage, SystemMessage
from prompt import router_instructions, doc_grader_instructions, doc_grader_prompt, rag_prompt, hallucination_grader_instructions
from langchain.text_splitter import CharacterTextSplitter

# Load environment variables
#------------------------------------------------------------------------------
load_dotenv()

# Set additional environment variables
os.environ["TOKENIZERS_PARALLELISM"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "local_llama_rag"

# Search
#------------------------------------------------------------------------------
web_search_tool = TavilySearchResults(k=3)

# LLM
#------------------------------------------------------------------------------
local_llm = 'llama3.3:70b-instruct-q2_K'
llm = ChatOllama(model=local_llm, temperature=0)
llm_json_mode = ChatOllama(model=local_llm, temperature=0, format="json")

# Document processing
#------------------------------------------------------------------------------
def clean_text(text: str) -> str:
    """Clean text from special characters and formatting issues"""
    import re
    # Remove special characters that look like dots or boxes
    text = re.sub(r'[\.]{3,}', ' ', text)
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove page numbers
    text = re.sub(r'\n\d+\n', '\n', text)
    return text.strip()

def process_pdf_to_vectorstore(pdf_path: str, persist_directory: str = "storage/vectorstore"):
    # Load PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    # Clean the text content of each document
    for doc in documents:
        doc.page_content = clean_text(doc.page_content)
    
    # Create text splitter with specific parameters for PDF content
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=2000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
        strip_whitespace=True
    )
    
    # Split documents
    texts = text_splitter.split_documents(documents)
    
    # Additional filtering to remove very short chunks or table of contents
    texts = [t for t in texts if len(t.page_content.strip()) > 100 and not t.page_content.count('...') > 3]
    
    print(f"Created {len(texts)} chunks from the PDF")
    
    # Create embeddings
    embeddings = NomicEmbeddings(
        model="nomic-embed-text-v1.5",
        inference_mode="local"
    )
    
    # Create and persist vector store
    vectorstore = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    
    return vectorstore

def print_random_chunk(vectorstore):
    """Retrieve and print a random chunk from the vector store"""
    import random
    
    # Get all document ids
    collection = vectorstore._collection
    ids = collection.get()['ids']
    
    # Select a random id
    random_id = random.choice(ids)
    
    # Retrieve the document
    result = collection.get(ids=[random_id])
    
    # Print the chunk content and metadata
    print("\n=== Random Chunk ===")
    print("Content:", result['documents'][0])
    print("\nMetadata:", result['metadatas'][0])
    print("===================\n")


def print_router_test(llm_json_mode):
    """Test the router with different types of questions"""
    test_web_search = llm_json_mode.invoke(
        [SystemMessage(content=router_instructions)]
        + [
            HumanMessage(
                content="quand est-ce que le mieux vivre 2024 est sorti?"
            )
        ]
    )
    test_web_search_2 = llm_json_mode.invoke(
        [SystemMessage(content=router_instructions)]
        + [HumanMessage(content="What are the models released today for llama3.2?")]
    )
    test_vector_store = llm_json_mode.invoke(
        [SystemMessage(content=router_instructions)]
        + [HumanMessage(content="quand est-ce que un bebe a ses premieres dents?")]
    )
    print(
        json.loads(test_web_search.content),
        json.loads(test_web_search_2.content),
        json.loads(test_vector_store.content),
    )

# Initialize vector store
#------------------------------------------------------------------------------
pdf_path = '/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/reliable_rag_agent/storage/mieuxvivre2024_guide_complet.pdf'
vectorstore = process_pdf_to_vectorstore(pdf_path)

# Print a random chunk to test
#print_random_chunk(vectorstore)

# print router test
#print_router_test(llm_json_mode)

# Create retriever with search parameters
retriever = vectorstore.as_retriever(k = 5)

#print(retriever.invoke("quand est-ce que le mieux vivre 2024 est sorti?"))

Question = 'quand est-ce que les dents des bébés apparaissent?'
docs = retriever.invoke(Question)
doc_txt = docs[1].page_content
doc_grader_prompt_formatted = doc_grader_prompt.format(document=doc_txt, question=Question)
result = llm_json_mode.invoke([SystemMessage(content=doc_grader_instructions), HumanMessage(content=doc_grader_prompt_formatted)])
#print(json.loads(result.content))
#print(doc_txt)
print('--------------------------------')
rag_prompt_formatted = rag_prompt.format(context=doc_txt, question=Question)
generation = llm.invoke([HumanMessage(content=rag_prompt_formatted)])
print(generation.content)
print('--------------------------------')
