from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base

class SingleVibePrompt(Base):
    __tablename__ = "single_vibe_prompts"
    prompt_id = Column(String, primary_key=True, index=True)
    prompt_text = Column(String, nullable=False)
    prompt_type = Column(String, nullable=False)  # 'emotion_checkin' or 'contextual_followup'
    emotion_tag = Column(String, nullable=True)  # used only for contextual
    options = Column(Text, nullable=True)  # JSON string of options
    allow_other = Column(String, nullable=True)  # 'true' or 'false'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
