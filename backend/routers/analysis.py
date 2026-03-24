from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional
from services.llm_service import LLMService

router = APIRouter()
llm = LLMService()

class AnalysisRequest(BaseModel):
    content: str
    analysis_type: Optional[str] = "summary"

class ReportRequest(BaseModel):
    include_sales: Optional[bool] = True
    include_finance: Optional[bool] = True
    include_forecast: Optional[bool] = True

@router.post("/document")
async def analyze_document(body: AnalysisRequest, request: Request):
    result = await llm.analyze_document(body.content, body.analysis_type)
    return {"analysis": result, "type": body.analysis_type}

@router.post("/report")
async def generate_report(body: ReportRequest, request: Request):
    rag = request.app.state.rag
    ml = request.app.state.ml
    kpis = ml.get_kpis()
    chunks = rag.retrieve("sales revenue performance finance", top_k=6)
    context = "\n".join([c["content"] for c in chunks])
    data = {"kpis": kpis, "business_context": context}
    result = await llm.generate_report(data)
    return {"report": result, "kpis": kpis}

@router.get("/kpis")
async def get_kpis(request: Request):
    ml = request.app.state.ml
    return ml.get_kpis()

@router.get("/anomalies")
async def get_anomalies(request: Request):
    ml = request.app.state.ml
    anomalies = ml.detect_anomalies()
    return {"anomalies": anomalies, "count": len(anomalies)}
