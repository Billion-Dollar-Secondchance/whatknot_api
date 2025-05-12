# app/db/models/mystery_moodbox.py

import uuid
import enum
from sqlalchemy import (
    Column,
    String,
    Text,
    Date,
    Time,
    DateTime,
    ForeignKey
)
from uuid import uuid4
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SQLEnum
from app.db.database import Base
from datetime import datetime


class MoodStatusEnum(str, enum.Enum):
    PROMPTED = "prompted"
    ANSWERED = "answered"
    GUESSED = "guessed"
    RESPONDED = "responded"
    EXPIRED = "expired"


class MysteryMoodbox(Base):
    __tablename__ = "mystery_moodbox"

    mood_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    pair_id = Column(String, ForeignKey("partner_pairing.pair_id", ondelete="CASCADE"), nullable=False)

    prompt_date = Column(Date, nullable=False)
    prompt_time = Column(Time, nullable=False)

    # prompted_user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    mood = Column(String, nullable=True)
    explanation = Column(Text, nullable=True)

    mood_status = Column(
        SQLEnum(MoodStatusEnum, name="moodstatusenum", native_enum=False),
        default=MoodStatusEnum.PROMPTED,
        nullable=False
    )

    question_id = Column(
        UUID(as_uuid=True),
        ForeignKey("mystery_moodbox_questions.question_id", ondelete="CASCADE"),
        nullable=False
    )

    # guesser_id = Column(String, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)
    guess_text = Column(Text, nullable=True)
    guessed_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    prompted_user_id = Column(String, ForeignKey("public.users.user_id", ondelete="CASCADE"), nullable=False)
    guesser_id = Column(String, ForeignKey("public.users.user_id", ondelete="SET NULL"), nullable=True)


