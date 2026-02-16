from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.db.session import SessionLocal
from app.models.lead import Lead, LeadStatus
from app.services.followup_service import (
    send_followup_24h,
    send_followup_48h,
    send_followup_72h,
)
from app.core.config import get_settings

settings = get_settings()

scheduler = AsyncIOScheduler(timezone="UTC")


def _get_db() -> Session:
    return SessionLocal()


async def check_followups():
    db = _get_db()
    try:
        now = datetime.now(timezone.utc)

        leads = (
            db.query(Lead)
            .filter(
                Lead.next_followup_at != None,  # noqa
                Lead.next_followup_at <= now,
                Lead.status != LeadStatus.BOOKED,
            )
            .all()
        )

        for lead in leads:
            if (
                lead.followup_state
                and not lead.followup_state.sent_24h
                and lead.status == LeadStatus.CONTACTED
            ):
                await send_followup_24h(db, lead)

            elif (
                lead.followup_state
                and lead.followup_state.sent_24h
                and not lead.followup_state.sent_48h
            ):
                await send_followup_48h(db, lead)

            elif (
                lead.followup_state
                and lead.followup_state.sent_48h
                and not lead.followup_state.sent_72h
            ):
                await send_followup_72h(db, lead)

            else:
                if lead.status != LeadStatus.BOOKED:
                    lead.status = LeadStatus.NO_RESPONSE

            # Commit after each lead update
            db.commit()

    finally:
        db.close()


def start_scheduler():
    scheduler.add_job(
        check_followups,
        "interval",
        seconds=settings.FOLLOWUP_CHECK_INTERVAL_SECONDS,
        id="followup_checker",
        replace_existing=True,
    )
    scheduler.start()