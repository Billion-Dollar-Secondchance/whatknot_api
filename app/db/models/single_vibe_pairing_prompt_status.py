from sqlalchemy import Column, String, Integer, Date, Boolean, UniqueConstraint
from app.db.base import Base

class SingleVibePairingPromptStatus(Base):
    __tablename__ = "single_vibe_pairing_prompt_status"

    pairing_prompt_id = Column(String, primary_key=True, index=True)
    user_1_id = Column(String)
    user_2_id = Column(String)
    match_count = Column(Integer, default=1)
    last_matched_on = Column(Date)
    prompted = Column(Boolean, default=False)  # if pair-up prompt was sent
    active = Column(Boolean, default=True)     # if pairing streak is still alive

    __table_args__ = (
        UniqueConstraint('user_1_id', 'user_2_id', name='uq_pair_unique'),
    )
