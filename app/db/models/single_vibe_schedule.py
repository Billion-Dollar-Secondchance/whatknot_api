from sqlalchemy import Column, String, Date, ForeignKey
from app.db.base import Base

class SingleVibeSchedule(Base):
    __tablename__ = "single_vibe_schedule"
    schedule_id = Column(String, primary_key=True, index=True)
    vibe_id = Column(String, ForeignKey("single_vibe_definitions.vibe_id"), nullable=False)
    scheduled_date = Column(Date, nullable=False)
