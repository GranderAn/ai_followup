from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum


class MessageType(str, enum.Enum):
    INSTANT = "instant"
    F24 = "24h"
    F48 = "48h"
    F72 = "72h"
    OBJECTION = "objection"
    REVIVAL = "revival"
    BOOKING_CONFIRMATION = "booking_confirmation"


class MessageLog(Base):
    __tablename__ = "message_logs"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    message_type = Column(Enum(MessageType), nullable=False)
    content = Column(Text, nullable=False)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())

    lead = relationship("Lead", back_populates="messages")