from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base

class SingleVibeEntry(Base):
    __tablename__ = "single_vibe_entries"

    single_vibe_id = Column(String, primary_key=True, index=True)  # e.g., sv_000001
    user_id = Column(String, nullable=False, index=True)
    vibe = Column(String, nullable=False)
    prompt_answers = Column(Text, nullable=True)  # Stored as JSON string
    answer_status = Column(String, nullable=False, default="incomplete")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
