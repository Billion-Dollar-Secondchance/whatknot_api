# app/schemas/badge.py

from pydantic import BaseModel
from typing import Optional

class BadgeCreate(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    min_streak: Optional[int] = None
    min_matches: Optional[int] = None
    badge_type: Optional[str] = "emotional"

