from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models.lead import Lead, LeadStatus
from app.models.message_log import MessageLog, MessageType
from app.models.followup_state import FollowUpState
from app.services.ai_service import generate_message
from app.services.email_service import send_email


BUSINESS_NAME = "Your Business"
BOOKING_LINK = "https://your-booking-link.com"


def _now() -> datetime:
    return datetime.now(timezone.utc)


async def send_instant_response(db: Session, lead: Lead) -> None:
    content = await generate_message(
        message_type="instant",
        business_name=BUSINESS_NAME,
        service=lead.service,
        lead_name=lead.name,
        booking_link=BOOKING_LINK,
    )
    await send_email(lead.email, "Thanks for reaching out", content)

    log = MessageLog(
        lead_id=lead.id,
        message_type=MessageType.INSTANT,
        content=content,
    )
    db.add(log)

    lead.status = LeadStatus.CONTACTED
    lead.last_message_at = _now()
    lead.next_followup_at = _now() + timedelta(hours=24)

    if not lead.followup_state:
        lead.followup_state = FollowUpState(lead_id=lead.id)

    db.commit()
    db.refresh(lead)


async def send_followup_24h(db: Session, lead: Lead) -> None:
    if lead.status == LeadStatus.BOOKED:
        return

    content = await generate_message(
        message_type="24h",
        business_name=BUSINESS_NAME,
        service=lead.service,
        lead_name=lead.name,
        booking_link=BOOKING_LINK,
    )
    await send_email(lead.email, "Quick follow-up", content)

    log = MessageLog(
        lead_id=lead.id,
        message_type=MessageType.F24,
        content=content,
    )
    db.add(log)

    lead.status = LeadStatus.F24
    lead.last_message_at = _now()
    lead.next_followup_at = _now() + timedelta(hours=24)
    lead.followup_state.sent_24h = True

    db.commit()
    db.refresh(lead)


async def send_followup_48h(db: Session, lead: Lead) -> None:
    if lead.status == LeadStatus.BOOKED:
        return

    content = await generate_message(
        message_type="48h",
        business_name=BUSINESS_NAME,
        service=lead.service,
        lead_name=lead.name,
        booking_link=BOOKING_LINK,
    )
    await send_email(lead.email, "Still interested?", content)

    log = MessageLog(
        lead_id=lead.id,
        message_type=MessageType.F48,
        content=content,
    )
    db.add(log)

    lead.status = LeadStatus.F48
    lead.last_message_at = _now()
    lead.next_followup_at = _now() + timedelta(hours=24)
    lead.followup_state.sent_48h = True

    db.commit()
    db.refresh(lead)


async def send_followup_72h(db: Session, lead: Lead) -> None:
    if lead.status == LeadStatus.BOOKED:
        return

    content = await generate_message(
        message_type="72h",
        business_name=BUSINESS_NAME,
        service=lead.service,
        lead_name=lead.name,
        booking_link=BOOKING_LINK,
    )
    await send_email(lead.email, "Last quick check-in", content)

    log = MessageLog(
        lead_id=lead.id,
        message_type=MessageType.F72,
        content=content,
    )
    db.add(log)

    lead.status = LeadStatus.F72
    lead.last_message_at = _now()
    lead.next_followup_at = _now() + timedelta(days=7)
    lead.followup_state.sent_72h = True

    db.commit()
    db.refresh(lead)