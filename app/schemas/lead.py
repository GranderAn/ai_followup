from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.lead import LeadStatus


class LeadCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    service: str
    source: Optional[str] = None


class LeadRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str]
    service: str
    source: Optional[str]
    status: LeadStatus
    created_at: datetime
    updated_at: datetime
    last_message_at: Optional[datetime]
    next_followup_at: Optional[datetime]

    model_config = {
    "from_attributes": True
}