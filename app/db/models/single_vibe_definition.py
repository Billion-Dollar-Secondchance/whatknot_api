from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class SingleVibeDefinition(Base):
    __tablename__ = "single_vibe_definitions"
    vibe_id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
