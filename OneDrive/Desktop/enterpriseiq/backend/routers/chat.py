from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List, Dict, Optional
from services.llm_service import LLMService

router = APIRouter()
llm = LLMService()

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = "default"
    history: Optional[List[Dict]] = []

@router.post("/ask")
async def ask(body: ChatRequest, request: Request):
    rag = request.app.state.rag
    chunks = rag.retrieve(body.query)
    result = await llm.chat_with_rag(body.query, chunks, body.history or [])
    return result
