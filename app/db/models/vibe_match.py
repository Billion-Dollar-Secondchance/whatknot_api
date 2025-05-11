# # File: app/db/models/vibe_match.py

# from sqlalchemy import Column, String, ForeignKey, Enum, Integer, Float, DateTime, Boolean, JSON
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import relationship
# import uuid
# from datetime import datetime
# from app.db.base import Base

# class VibeQuestion(Base):
#     __tablename__ = "vibe_questions"
#     question_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     question_text = Column(String, nullable=False)
#     question_type = Column(Enum(
#         "text",
#         "date_picker",
#         "time_picker",
#         "swipe",
#         "single_choice",
#         "multi_choice",
#         "true_false",
#         "emoji_choice",
#         "image_choice",
#         "scale_rating",
#         name="vibe_question_type"
#     ), nullable=False)
#     options = Column(JSON, nullable=True)
#     is_active = Column(Boolean, default=True)
#     created_at = Column(DateTime, default=datetime.utcnow)


# class VibeMatch(Base):
#     __tablename__ = "vibe_matches"
#     vibe_match_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     pair_id = Column(UUID(as_uuid=True), nullable=False)
#     num_questions = Column(Integer, nullable=False)
#     started_by = Column(String, nullable=False)  # user_id
#     status = Column(Enum("started", "completed", name="vibe_match_status"), default="started")
#     created_at = Column(DateTime, default=datetime.utcnow)


# class VibeMatchQuestion(Base):
#     __tablename__ = "vibe_match_questions"
#     vibe_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     vibe_match_id = Column(UUID(as_uuid=True), ForeignKey("vibe_matches.vibe_match_id"), nullable=False)
#     question_id = Column(UUID(as_uuid=True), ForeignKey("vibe_questions.question_id"), nullable=False)
#     order_number = Column(Integer, nullable=True)
#     created_at = Column(DateTime, default=datetime.utcnow)


# class VibeMatchResponse(Base):
#     __tablename__ = "vibe_match_responses"
#     vibe_response_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     vibe_match_id = Column(UUID(as_uuid=True), ForeignKey("vibe_matches.vibe_match_id"), nullable=False)
#     question_id = Column(UUID(as_uuid=True), ForeignKey("vibe_questions.question_id"), nullable=False)
#     user_id = Column(String, nullable=False)
#     answer = Column(String, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)

# class VibeQuestionDayMapping(Base):
#     __tablename__ = "vibe_question_day_mapping"
#     mapping_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     question_id = Column(UUID(as_uuid=True), ForeignKey("vibe_questions.question_id"), nullable=False)
#     days_condition = Column(String, nullable=False)  # e.g., "<1", "=2", ">5", ">=3 and <=6"
#     created_at = Column(DateTime, default=datetime.utcnow)

# File: app/db/models/vibe_match.py

from sqlalchemy import Column, String, Boolean, DateTime, Enum, ForeignKey, Integer, JSON, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid
import enum
import datetime

class VibeQuestion(Base):
    __tablename__ = "vibe_questions"
    question_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_text = Column(String, nullable=False)
    question_type = Column(Enum(
        "text", "date_picker", "time_picker", "swipe",
        "single_choice", "multi_choice", "true_false",
        "emoji_choice", "image_choice", "scale_rating",
        name="vibe_question_type"
    ), nullable=False)
    options = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class VibeQuestionDayMapping(Base):
    __tablename__ = "vibe_question_day_mapping"
    mapping_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id = Column(UUID(as_uuid=True), ForeignKey("vibe_questions.question_id"), nullable=False)
    days_condition = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class VibeQuestionDateMapping(Base):
    __tablename__ = "vibe_question_date_mapping"
    mapping_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id = Column(UUID(as_uuid=True), ForeignKey("vibe_questions.question_id"), nullable=False)
    scheduled_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class VibeMatch(Base):
    __tablename__ = "vibe_matches"
    vibe_match_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pair_id = Column(UUID(as_uuid=True), nullable=False)
    num_questions = Column(Integer, nullable=False)
    started_by = Column(String, nullable=False)
    status = Column(Enum("started", "completed", name="vibe_match_status"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class VibeMatchResponse(Base):
    __tablename__ = "vibe_match_responses"
    vibe_response_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vibe_match_id = Column(UUID(as_uuid=True), ForeignKey("vibe_matches.vibe_match_id"), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("vibe_questions.question_id"), nullable=False)
    user_id = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
