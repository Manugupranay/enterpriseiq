from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from services.mcp_service import MCPService

router = APIRouter()
mcp = MCPService()

class EmailRequest(BaseModel):
    recipient: str
    subject: str
    content: str

class MeetingRequest(BaseModel):
    title: str
    date: str
    time: str
    attendees: str

@router.post("/send-report")
async def send_report(body: EmailRequest):
    result = await mcp.send_report_email(body.recipient, body.subject, body.content)
    return result

@router.post("/schedule-meeting")
async def schedule_meeting(body: MeetingRequest):
    result = await mcp.schedule_review_meeting(body.title, body.date, body.time, body.attendees)
    return result
