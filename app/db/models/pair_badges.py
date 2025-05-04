# app/db/models/pair_badges.py
from sqlalchemy import Column, String,DateTime, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.sql import func
import uuid

class PairBadge(Base):
    __tablename__ = "pair_badges"

    pair_badge_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    pair_id = Column(String, ForeignKey("partner_pairing.pair_id", ondelete="CASCADE"), nullable=False)
    badge_id = Column(String, ForeignKey("badge_definitions.badge_id", ondelete="CASCADE"), nullable=False)
    awarded_at = Column(DateTime(timezone=True), server_default=func.now())

    badge = relationship("BadgeDefinition", backref="pair_badges")

    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # pair_id = Column(String, ForeignKey("partner_pairing.pair_id", ondelete="CASCADE"), nullable=False)
    # badge_id = Column(UUID(as_uuid=True), ForeignKey("badge_definitions.id", ondelete="CASCADE"), nullable=False)
    # awarded_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    # badge = relationship("BadgeDefinition")
