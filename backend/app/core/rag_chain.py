from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
import os

# Initialize components
embeddings = OpenAIEmbeddings()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)
vector_store = None

# Initialize LangChain chat model with GPT-4
chat_model = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.7,
    max_tokens=1000
)

def get_qa_chain():
    """Get or create the QA chain with current vector store."""
    if vector_store is None:
        return None
    
    # Create retriever with top 3 chunks
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )
    
    # Create QA chain
    return RetrievalQA.from_chain_type(
        llm=chat_model,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

def process_and_store_chunks(chunks):
    """Process text chunks and store in vector database."""
    global vector_store
    if vector_store is None:
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings
        )
    else:
        vector_store.add_documents(chunks) 