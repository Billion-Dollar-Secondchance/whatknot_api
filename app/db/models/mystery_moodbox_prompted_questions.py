from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, Enum,Text,Boolean,DateTime,Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum
import uuid
from sqlalchemy.sql import func
from pydantic import BaseModel
from datetime import datetime  # also at the top if not already there


class PromptStatusEnum(str, enum.Enum):
    prompted = "prompted"
    guessed = "guessed"
    answered_by_one = "answered_by_one"
    answered_by_both = "answered_by_both"


class MysteryMoodboxPromptedQuestion(Base):
    __tablename__ = "mystery_moodbox_prompted_questions"

    prompt_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pair_id = Column(String, ForeignKey("partner_pairing.pair_id", ondelete="CASCADE"), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("mystery_moodbox_questions.question_id", ondelete="CASCADE"), nullable=False)
    prompted_user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    prompt_status = Column(Enum(PromptStatusEnum, name="promptstatusenum"), nullable=False, default=PromptStatusEnum.prompted)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    question = relationship("MysteryMoodboxQuestion", backref="prompted_questions")
    guesser_id = Column(String, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)
    guess_text = Column(Text, nullable=True)
    answer = Column(Text, nullable=True)
    guessed_at = Column(TIMESTAMP(timezone=True), nullable=True)
    answer_matched = Column(Boolean, nullable=True)


class SubmitPromptResponse(BaseModel):
    prompt_id: UUID
    answer: str

    class Config:
        arbitrary_types_allowed = True

class MysteryMoodboxDateMapping(Base):
    __tablename__ = "mystery_moodbox_date_mapping"

    mapping_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id = Column(UUID(as_uuid=True), ForeignKey("mystery_moodbox_questions.question_id"), nullable=False)
    scheduled_date = Column(Date, nullable=False)
    pair_days_condition = Column(String, nullable=False)  # "<3", "=1", etc
    created_at = Column(DateTime, default=func.now())





