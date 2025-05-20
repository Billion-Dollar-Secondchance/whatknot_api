from sqlalchemy import Column, String, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class SingleVibePromptResponse(Base):
    __tablename__ = "single_vibe_prompt_response"

    vibe_response_id = Column(String, primary_key=True)  # ✅ must match this
    prompt_schedule_id = Column(String, ForeignKey("single_vibe_prompt_schedule.prompt_schedule_id"))
    prompt_id = Column(String, ForeignKey("single_vibe_prompts.prompt_id"))
    user_id = Column(String, ForeignKey("users.user_id"))
    answer = Column(String, nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
