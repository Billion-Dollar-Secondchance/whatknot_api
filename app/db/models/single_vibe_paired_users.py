from sqlalchemy import Column, String, ForeignKey, Date, Integer,Boolean,DateTime
from app.db.base import Base
from sqlalchemy.sql import func

class SingleVibePairedUser(Base):
    __tablename__ = "single_vibe_paired_users"

    pair_id = Column(String, primary_key=True)
    user_1_id = Column(String)
    user_2_id = Column(String)
    paired_on = Column(DateTime, default=func.now())