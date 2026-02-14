from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class CalendlyInvitee(BaseModel):
    email: EmailStr


class CalendlyEvent(BaseModel):
    start_time: datetime  # ISO 8601 from Calendly


class CalendlyPayload(BaseModel):
    event: CalendlyEvent
    invitee: CalendlyInvitee

    model_config = {
        "from_attributes": True
    }