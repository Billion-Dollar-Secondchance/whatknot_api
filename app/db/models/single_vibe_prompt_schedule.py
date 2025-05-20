from sqlalchemy import Column, String, Date, ForeignKey
from app.db.base import Base

class SingleVibePromptSchedule(Base):
    __tablename__ = "single_vibe_prompt_schedule"
    prompt_schedule_id = Column(String, primary_key=True, index=True)
    prompt_id = Column(String, ForeignKey("single_vibe_prompts.prompt_id"), nullable=False)
    emotion_tag = Column(String, nullable=False) 
    scheduled_date = Column(Date, nullable=False)

