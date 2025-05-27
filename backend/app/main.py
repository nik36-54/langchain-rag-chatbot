from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .routes import upload, chat

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="LLM Chatbot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to the LLM Chatbot API",
        "endpoints": {
            "/api/upload": "POST - Upload PDF files for processing",
            "/api/chat": "POST - Send chat messages and get RAG-based responses"
        }
    } 