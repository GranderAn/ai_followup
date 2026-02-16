from fastapi import FastAPI
from app.core.config import get_settings
from app.api.routes import leads, booking, webhooks
from app.db.session import engine
from app.db.base import Base
from app.workers.scheduler import start_scheduler

settings = get_settings()

# Temporary: auto-create tables during early development
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Follow-Up System")


@app.on_event("startup")
async def startup_event():
    start_scheduler()


# API routes
app.include_router(leads.router, prefix=settings.API_V1_STR)
app.include_router(booking.router, prefix=settings.API_V1_STR)
app.include_router(webhooks.router, prefix="/api/v1")


@app.get("/")
def health_check():
    return {"status": "ok"}