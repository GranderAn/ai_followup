from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.lead import Lead, LeadStatus
from app.models.booking import Booking
from app.schemas.calendly import CalendlyPayload
from app.services.calendly_signature import verify_calendly_signature


router = APIRouter(prefix="/webhooks", tags=["webhooks"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/calendly")
async def calendly_webhook(
    payload: CalendlyPayload,
    db: Session = Depends(get_db),
):
    await verify_calendly_signature(request)

    raw = await request.json()
    payload = CalendlyPayload(**raw)
    
    email = payload.invitee.email
    scheduled_for = payload.event.start_time

    lead = db.query(Lead).filter(Lead.email == email).first()
    if not lead:
        return {"status": "ignored"}

    # Check if booking already exists
    booking = db.query(Booking).filter(Booking.lead_id == lead.id).first()

    if booking:
        # Update existing booking
        booking.scheduled_for = scheduled_for
        booking.source = "calendly"
    else:
        # Create new booking
        booking = Booking(
            lead_id=lead.id,
            scheduled_for=scheduled_for,
            source="calendly",
        )
        db.add(booking)

    lead.status = LeadStatus.BOOKED
    lead.booking = booking
    lead.next_followup_at = None

    db.commit()
    return {"status": "ok"}



