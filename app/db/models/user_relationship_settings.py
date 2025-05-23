from sqlalchemy import Column, String, Date, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY
from app.db.base import Base

class UserRelationshipSettings(Base):
    __tablename__ = "user_relationship_settings"

    settings_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    pair_id = Column(String, ForeignKey("single_vibe_paired_users.pair_id"), nullable=True)

    # Common fields
    intentions = Column(ARRAY(String), nullable=True)           # Multi-select (same for both)
    relationship_type = Column(String, nullable=True)           # Dating, Married, etc.
    living_situation = Column(String, nullable=True)            # Living setup

    # Optional extras
    anniversary = Column(Date, nullable=True)
    current_emotion = Column(String, nullable=True)             # Singles: Hopeful, Curious, etc.
    preferred_relationship_type = Column(String, nullable=True) # For singles: what they're looking for

    is_active_pair = Column(Boolean, default=False)             # Used only for paired users
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
