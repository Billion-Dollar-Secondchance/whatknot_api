# 📄 File: app/api/routes/user_relationship_settings.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from app.dependencies.auth import get_current_user, get_db
from app.db.models.user import User
from app.db.models.user_relationship_settings import UserRelationshipSettings
from app.utils.id_generator import generate_relationship_settings_id
from app.utils.response_format import success_response, failure_response
from datetime import datetime
from app.db.models.single_vibe_paired_users import SingleVibePairedUser


router = APIRouter()

# ✅ Schema for updating relationship settings
class UpdateRelationshipSettings(BaseModel):
    intentions: Optional[List[str]] = None
    relationship_type: Optional[str] = None
    living_situation: Optional[str] = None
    anniversary: Optional[str] = None
    current_emotion: Optional[str] = None
    preferred_relationship_type: Optional[str] = None

# ✅ GET: Fetch current user's relationship settings
@router.get("/relationship/settings")
def get_relationship_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    settings = db.query(UserRelationshipSettings).filter_by(user_id=current_user.user_id).first()

    if not settings:
        return success_response("No relationship settings found", None)

    days_together = None

    # ✅ Calculate days_together only if a valid pair_id exists
    if settings.pair_id:
        try:
            pair = db.query(SingleVibePairedUser).filter_by(pair_id=settings.pair_id).first()
            if pair and pair.paired_on:
                days_together = (datetime.utcnow().date() - pair.paired_on.date()).days
            else:
                days_together = None  # Pair not found or missing date
        except Exception as e:
            print(f"❌ Error calculating days_together: {e}")
            days_together = None

    return success_response("Relationship settings fetched", {
        "intentions": settings.intentions,
        "relationship_type": settings.relationship_type,
        "living_situation": settings.living_situation,
        "anniversary": settings.anniversary,
        "current_emotion": settings.current_emotion,
        "preferred_relationship_type": settings.preferred_relationship_type,
        "is_active_pair": settings.is_active_pair,
        "pair_id": settings.pair_id,
        "days_together": days_together
    })



# ✅ POST: Create or update relationship settings (partial update supported)
@router.post("/relationship/updatesettings")
def update_relationship_settings(
    payload: UpdateRelationshipSettings,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    settings = db.query(UserRelationshipSettings).filter_by(user_id=current_user.user_id).first()

    if settings:
        # Update only provided fields
        for field, value in payload.dict(exclude_unset=True).items():
            setattr(settings, field, value)
        settings.updated_at = datetime.utcnow()
    else:
        # Create new entry
        settings = UserRelationshipSettings(
            settings_id=generate_relationship_settings_id(db),
            user_id=current_user.user_id,
            pair_id=getattr(current_user, 'pair_id', None),
            **payload.dict(exclude_unset=True)
        )
        db.add(settings)

    db.commit()
    return success_response("Relationship settings updated")
