from sqlalchemy import Column, Integer, Text, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP
from app.db.database import Base

class MysteryMoodboxSession(Base):
    __tablename__ = "mystery_moodbox_sessions"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('mystery_moodbox_questions.id', ondelete='CASCADE'), nullable=False)
    asker_user_id = Column(UUID(as_uuid=True), nullable=False)
    responder_user_id = Column(UUID(as_uuid=True), nullable=False)
    responder_answer = Column(Text, nullable=True)
    is_correct = Column(Boolean, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
