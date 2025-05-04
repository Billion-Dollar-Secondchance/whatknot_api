# app/db/models/mystery_moodbox_question.py
from enum import Enum as PyEnum
import uuid

from sqlalchemy import Column, String, Enum, Text, ForeignKey,Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# 1) Import Base from base.py
from app.db.base import Base

# 2) Import the PartnerPairing model so it's registered
from app.db.models.partner_pairing import PartnerPairing  


class CreatedByType(PyEnum):
    ADMIN = "admin"
    USER = "user"

class QuestionType(PyEnum):
    INPUT_TEXT = "input_text"
    SINGLE_CHOICE = "single_choice"
    MULTI_CHOICE = "multi_choice"


class MysteryMoodboxQuestion(Base):
    __tablename__ = "mystery_moodbox_questions"

    # id = Column(Integer, primary_key=True, index=True) 
    question_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pair_id = Column(
        String,
        ForeignKey("partner_pairing.pair_id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    
    created_by_type = Column(Enum(CreatedByType), nullable=False)
    submitted_by = Column(String, nullable=True)
    question_type = Column(
        Enum("input_text", "single_choice", "multi_choice", name="questiontype"),
        nullable=False,
        server_default="input_text"
    )
    question_text = Column(Text, nullable=False)
    options = Column(JSONB, nullable=True)
    correct_answer = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    partner_pairing = relationship(
        "PartnerPairing",
        backref="mystery_moodbox_questions",
        lazy="subquery"
    )
