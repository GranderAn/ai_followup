from app.db.base_class import Base

# Import all models so Alembic can detect them
from app.models.lead import Lead
from app.models.message_log import MessageLog
from app.models.booking import Booking
from app.models.followup_state import FollowUpState