# app/db/models/day_question_mapping.py
import uuid
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base

class DayQuestionMapping(Base):
    __tablename__ = "day_question_mapping"

    # how many days since pairing
    days_since_paired = Column(Integer, primary_key=True)

    # which question to send
    question_id = Column(
        UUID(as_uuid=True),
        ForeignKey("mystery_moodbox_questions.question_id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
