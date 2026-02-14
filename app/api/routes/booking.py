from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.session import SessionLocal
from app.models.lead import Lead, LeadStatus
from app.models.booking import Booking
from app.schemas.booking import BookingConfirmed


router = APIRouter(prefix="/booking", tags=["booking"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/confirmed")
async def booking_confirmed(
    payload: BookingConfirmed,
    db: Session = Depends(get_db),
):
    lead_id = payload.lead_id
    scheduled_for = payload.scheduled_for

    # Find the lead
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        return {"status": "ignored"}

    # Check if a booking already exists for this lead
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

    # Update lead status
    lead.status = LeadStatus.BOOKED
    lead.booking = booking
    lead.next_followup_at = None

    db.commit()
    return {"status": "ok"}
