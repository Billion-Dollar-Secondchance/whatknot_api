from sqlalchemy import Column, String, ForeignKey, Date, Integer,Boolean,DateTime
from app.db.base import Base
from sqlalchemy.sql import func

class SingleVibePairRequest(Base):
    __tablename__ = "single_vibe_pair_requests"

    request_id = Column(String, primary_key=True)
    sender_id = Column(String, ForeignKey("users.user_id"))
    receiver_id = Column(String, ForeignKey("users.user_id"))
    match_count = Column(Integer)
    requested_on = Column(DateTime, default=func.now())
    status = Column(String, default="pending")  # pending, accepted, rejected, expired
