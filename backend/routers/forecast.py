from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional
from services.llm_service import LLMService

router = APIRouter()
llm = LLMService()

class ForecastRequest(BaseModel):
    periods: Optional[int] = 6

@router.post("/revenue")
async def forecast_revenue(body: ForecastRequest, request: Request):
    ml = request.app.state.ml
    forecast_data = ml.forecast_revenue(body.periods)
    explanation = await llm.explain_forecast(forecast_data)
    return {**forecast_data, "explanation": explanation}

@router.get("/revenue")
async def get_forecast(request: Request):
    ml = request.app.state.ml
    return ml.forecast_revenue(6)
