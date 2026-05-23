"""
MCP Service — Google Suite Integration
Sends emails and creates calendar events via Anthropic MCP
"""

import os
import httpx
import json
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv(override=True)

CLAUDE_MODEL = "claude-sonnet-4-20250514"
API_URL = "https://api.anthropic.com/v1/messages"

MCP_SERVERS = [
    {"type": "url", "url": "https://gmail.mcp.claude.com/mcp", "name": "gmail"},
    {"type": "url", "url": "https://gcal.mcp.claude.com/mcp", "name": "gcal"},
]


class MCPService:
    def _get_headers(self):
        load_dotenv(override=True)
        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        return {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "anthropic-beta": "mcp-client-2025-04-04",
            "content-type": "application/json",
        }

    async def send_report_email(self, recipient: str, subject: str, report_content: str) -> Dict:
        prompt = f"""Send an email with this business intelligence report:
To: {recipient}
Subject: {subject}
Body: {report_content}

Please send this email via Gmail."""
        try:
            result = await self._call_mcp(prompt)
            return {"success": True, "message": f"Report sent to {recipient}", "detail": result}
        except Exception as e:
            return {"success": False, "message": f"Demo mode — email would be sent to {recipient}", "detail": str(e)}

    async def schedule_review_meeting(self, title: str, date: str, time: str, attendees: str) -> Dict:
        prompt = f"""Schedule a business review meeting:
Title: {title}
Date: {date}
Time: {time}
Attendees: {attendees}
Duration: 60 minutes
Description: Quarterly business review — EnterpriseIQ AI Analysis

Please create this calendar event."""
        try:
            result = await self._call_mcp(prompt)
            return {"success": True, "message": f"Meeting '{title}' scheduled for {date} at {time}", "detail": result}
        except Exception as e:
            return {"success": False, "message": f"Demo mode — meeting would be created: {title} on {date}", "detail": str(e)}

    async def _call_mcp(self, prompt: str) -> str:
        load_dotenv(override=True)
        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        payload = {
            "model": CLAUDE_MODEL,
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}],
            "mcp_servers": MCP_SERVERS,
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(API_URL, headers=self._get_headers(), json=payload)
            resp.raise_for_status()
            data = resp.json()
            texts = [b["text"] for b in data.get("content", []) if b.get("type") == "text"]
            return " ".join(texts)
