# app/db/models/partner_pairing.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())


class PartnerPairing(Base):
    __tablename__ = "partner_pairing"

    pair_id = Column(String, primary_key=True, index=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    partner_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    pair_status = Column(String, nullable=False, server_default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", foreign_keys=[user_id])
    partner = relationship("User", foreign_keys=[partner_id])
