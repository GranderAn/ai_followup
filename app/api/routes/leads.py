from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.lead import LeadCreate, LeadRead
from app.models.lead import Lead, LeadStatus
from app.services.followup_service import send_instant_response

router = APIRouter(prefix="/leads", tags=["leads"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/new", response_model=LeadRead)
async def create_lead(
    lead_in: LeadCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    lead = Lead(
        name=lead_in.name,
        email=lead_in.email,
        phone=lead_in.phone,
        service=lead_in.service,
        source=lead_in.source,
        status=LeadStatus.NEW,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)

    background_tasks.add_task(send_instant_response, db, lead)

    return lead