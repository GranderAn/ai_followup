from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class FollowUpState(Base):
    __tablename__ = "followup_states"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), unique=True, nullable=False)

    sent_24h = Column(Boolean, default=False)
    sent_48h = Column(Boolean, default=False)
    sent_72h = Column(Boolean, default=False)
    revived = Column(Boolean, default=False)

    lead = relationship("Lead", back_populates="followup_state")