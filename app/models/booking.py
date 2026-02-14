from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, unique=True, index=True)
    scheduled_for = Column(DateTime(timezone=True), nullable=False)
    confirmed_at = Column(DateTime(timezone=True), server_default=func.now())
    source = Column(String, nullable=True)

    lead = relationship("Lead", back_populates="booking")