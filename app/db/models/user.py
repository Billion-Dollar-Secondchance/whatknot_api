from sqlalchemy import Column, String, DateTime
from app.db.base import Base
from datetime import datetime
import uuid

class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    login_type = Column(String)
    vibe_as = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
