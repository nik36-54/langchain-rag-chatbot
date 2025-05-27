from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..core.rag_chain import get_qa_chain

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        qa_chain = get_qa_chain()
        if qa_chain is None:
            raise HTTPException(
                status_code=400,
                detail="No documents have been uploaded yet. Please upload a PDF first."
            )

        # Get response from QA chain
        response = qa_chain({"query": request.question})
        
        # Extract sources from response
        sources = [doc.page_content for doc in response["source_documents"]]
        
        return ChatResponse(
            answer=response["result"],
            sources=sources
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 