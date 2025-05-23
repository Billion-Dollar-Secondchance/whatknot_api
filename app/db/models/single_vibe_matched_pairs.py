from sqlalchemy import Column, String, ForeignKey, Date, UniqueConstraint
from app.db.base import Base

class SingleVibeMatchedPair(Base):
    __tablename__ = "single_vibe_matched_pairs"

    single_vibe_match_id = Column(String, primary_key=True, index=True)
    user_1_id = Column(String, ForeignKey("users.user_id"))
    user_2_id = Column(String, ForeignKey("users.user_id"))
    prompt_schedule_id = Column(String, ForeignKey("single_vibe_prompt_schedule.prompt_schedule_id"))
    matched_on = Column(Date, nullable=False)

    __table_args__ = (
        UniqueConstraint('user_1_id', 'user_2_id', 'prompt_schedule_id', name='uq_match_once_per_prompt'),
    )
