"""
LLM Service — Claude API wrapper for EnterpriseIQ
Handles all AI reasoning tasks
"""

import os
import httpx
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv(override=True)

CLAUDE_MODEL = "claude-sonnet-4-20250514"
API_URL = "https://api.anthropic.com/v1/messages"

SYSTEM_PROMPT = """You are EnterpriseIQ, an expert AI Finance & Sales Intelligence Agent.

You help business leaders and analysts:
- Analyze sales performance, revenue trends, and KPIs
- Identify underperforming regions, products, or teams
- Explain financial anomalies and root causes
- Forecast revenue and flag risks
- Generate executive-ready insights and recommendations

Your style:
- Be precise, data-driven, and concise
- Always cite the data source when answering
- Flag risks and opportunities clearly
- Use business language (not technical jargon)
- End answers with 1-2 actionable recommendations

You have access to company sales data, financial reports, and business metrics.
"""


class LLMService:
    def _get_headers(self):
        load_dotenv(override=True)
        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set in .env file")
        return {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

    async def chat_with_rag(self, query: str, rag_chunks: List[Dict], history: List[Dict]) -> Dict:
        context = "\n\n".join([
            f"[Source: {c['source']} | Score: {c.get('score','N/A')}]\n{c['content']}"
            for c in rag_chunks
        ])
        user_msg = f"""BUSINESS DATA CONTEXT:
{context}

ANALYST QUESTION:
{query}

Answer based on the data above. Be specific with numbers and cite sources."""

        messages = history + [{"role": "user", "content": user_msg}]
        response = await self._call_api(messages)
        return {
            "answer": response,
            "sources": [c["source"] for c in rag_chunks]
        }

    async def analyze_document(self, content: str, analysis_type: str) -> str:
        prompts = {
            "summary": f"Analyze this business document and provide: (1) Key metrics, (2) Top 3 insights, (3) Red flags, (4) Recommendations.\n\nDocument:\n{content}",
            "kpis": f"Extract all KPIs and metrics from this document. Format as a structured list with values and trends.\n\nDocument:\n{content}",
            "anomalies": f"Identify any anomalies, unusual patterns, or concerning trends in this data.\n\nDocument:\n{content}",
        }
        prompt = prompts.get(analysis_type, prompts["summary"])
        return await self._call_api([{"role": "user", "content": prompt}])

    async def generate_report(self, data: Dict) -> str:
        prompt = f"""Generate a professional executive summary report based on this sales data:

{data}

Include:
1. Executive Summary (2-3 sentences)
2. Key Performance Highlights
3. Areas of Concern
4. Strategic Recommendations
5. Next Steps

Format professionally for C-suite presentation."""
        return await self._call_api([{"role": "user", "content": prompt}])

    async def explain_forecast(self, forecast_data: Dict) -> str:
        prompt = f"""Explain this sales forecast to a business executive:

Forecast Data: {forecast_data}

Provide:
- What the forecast shows
- Key drivers behind the prediction
- Confidence level and risks
- What actions to take based on this forecast"""
        return await self._call_api([{"role": "user", "content": prompt}])

    async def _call_api(self, messages: List[Dict]) -> str:
        payload = {
            "model": CLAUDE_MODEL,
            "max_tokens": 2000,
            "system": SYSTEM_PROMPT,
            "messages": messages,
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(API_URL, headers=self._get_headers(), json=payload)
            resp.raise_for_status()
            return resp.json()["content"][0]["text"]
