
from pydantic import BaseModel
from datetime import datetime

class BookingConfirmed(BaseModel):
    lead_id: int
    scheduled_for: datetime

    model_config = {
        "from_attributes": True
    }