from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum


class LeadStatus(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    F24 = "24h_sent"
    F48 = "48h_sent"
    F72 = "72h_sent"
    NO_RESPONSE = "no_response"
    REENGAGED = "reengaged"
    BOOKED = "booked"


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=True)
    service = Column(String, nullable=False)
    source = Column(String, nullable=True)

    status = Column(Enum(LeadStatus), default=LeadStatus.NEW, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    last_message_at = Column(DateTime(timezone=True), nullable=True)
    next_followup_at = Column(DateTime(timezone=True), nullable=True)

    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=True)

    messages = relationship("MessageLog", back_populates="lead")
    booking = relationship("Booking", back_populates="lead", uselist=False)
    followup_state = relationship(
        "FollowUpState", back_populates="lead", uselist=False
    )