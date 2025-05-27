from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
import tempfile
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os

router = APIRouter()

class UploadResponse(BaseModel):
    message: str
    num_chunks: int

# Initialize components
embeddings = OpenAIEmbeddings()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)
vector_store = None

@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        # Load and process PDF
        loader = PyPDFLoader(temp_file_path)
        pages = loader.load()
        chunks = text_splitter.split_documents(pages)

        # Store in ChromaDB
        global vector_store
        if vector_store is None:
            vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings
            )
        else:
            vector_store.add_documents(chunks)

        # Clean up temporary file
        os.unlink(temp_file_path)

        return UploadResponse(
            message="PDF processed successfully",
            num_chunks=len(chunks)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 