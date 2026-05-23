"""
EnterpriseIQ — AI Finance & Sales Intelligence Agent
FastAPI backend with RAG + LLM + ML + MCP
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv(override=True)

from routers import chat, analysis, forecast, actions
from services.rag_service import RAGService
from services.ml_service import MLService

rag = RAGService()
ml = MLService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 EnterpriseIQ starting up...")
    await rag.initialize()
    ml.initialize()
    app.state.rag = rag
    app.state.ml = ml
    print("✅ All services ready.")
    yield
    print("🛑 EnterpriseIQ shutting down.")

app = FastAPI(
    title="EnterpriseIQ AI",
    description="AI Finance & Sales Intelligence Agent",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(forecast.router, prefix="/api/forecast", tags=["Forecast"])
app.include_router(actions.router, prefix="/api/actions", tags=["Actions"])

@app.get("/")
def root():
    return {"status": "EnterpriseIQ AI is running", "version": "1.0.0"}
