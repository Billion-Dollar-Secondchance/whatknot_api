# app/api/routes/badges.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.models.badge_definition import BadgeDefinition
from app.schemas.badge import BadgeCreate
from app.db.session import get_db
from app.utils.response_format import success_response

router = APIRouter()

@router.post("/admin/badges")
def create_badge(badge: BadgeCreate, db: Session = Depends(get_db)):
    new_badge = BadgeDefinition(
        name=badge.name,
        description=badge.description,
        image_url=badge.image_url,
        min_streak=badge.min_streak,
        min_matches=badge.min_matches,
        badge_type=badge.badge_type
    )
    db.add(new_badge)
    db.commit()
    db.refresh(new_badge)
    return success_response("Badge created successfully", data={"badge_id": new_badge.badge_id})
