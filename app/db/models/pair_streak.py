# app/db/models/pair_streak.py
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func
from app.db.base import Base
import uuid

class PairStreak(Base):
    __tablename__ = "pair_streaks"

    streak_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    pair_id = Column(String, ForeignKey("partner_pairing.pair_id", ondelete="CASCADE"), nullable=False)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
