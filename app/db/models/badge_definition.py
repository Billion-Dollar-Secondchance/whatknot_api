# app/db/models/badge_definition.py
from sqlalchemy import Column, String, Text,Integer,DateTime,func
from app.db.base import Base
import uuid

class BadgeDefinition(Base):
    __tablename__ = "badge_definitions"
    badge_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    image_url = Column(String)
    min_streak = Column(Integer, nullable=True)
    min_matches = Column(Integer, nullable=True)
    badge_type = Column(String, default="emotional")
    created_at = Column(DateTime(timezone=True), server_default=func.now())