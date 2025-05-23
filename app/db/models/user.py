from sqlalchemy import Column, String, DateTime, Boolean,Date
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy.orm import Session
from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")


class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)  # wk_000001 style
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    login_type = Column(String, nullable=False)  # 'email', 'google', 'guest'
    guest_token = Column(String, unique=True, nullable=True)
    device_id = Column(String, nullable=True) 
    # new Google fields:
    name = Column(String, nullable=True)
    profile_image = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    date_of_birth = Column(String, nullable=True)
    google_id = Column(String, unique=True, nullable=True)

    vibe_as = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    pairing_code = Column(String(6), unique=True, nullable=True)
    pairing_status = Column(String, nullable=False, server_default="single")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    role = Column(String, nullable=True, default="user")
    interested_in = Column(String, nullable=True)
    vibe_keywords = Column(String, nullable=True)  # "Empathetic,Curious"
    education = Column(String, nullable=True)
    location = Column(String, nullable=True)
    relationship_goal = Column(String, nullable=True)  # Long-term, Exploring
    onboarded = Column(Boolean, default=False)
    height = Column(String, nullable=True)
    audio_intro = Column(String, nullable=True)  # URL to uploaded audio
    video_intro = Column(String, nullable=True)  # URL to uploaded video
    image_gallery = Column(String, nullable=True)  # Comma-separated image URLs
    mobile_number = Column(String, nullable=True, unique=False)

    @property
    def created_at_ist(self):
        if self.created_at:
            return self.created_at.astimezone(IST)
        return None

# Utility function to generate new wk-style user_id
def generate_incremental_user_id(db: Session):
    last_user = (
        db.query(User)
        .filter(User.user_id.like("wk_%"))
        .order_by(User.created_at.desc())
        .first()
    )
    if last_user:
        try:
            last_num = int(last_user.user_id.split("_")[1])
        except (IndexError, ValueError):
            last_num = 0
    else:
        last_num = 0

    return f"wk_{last_num + 1:06d}"

