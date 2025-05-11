# # app/api/routes/earned-badges.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_user, get_db
from app.db.models.user import User
from app.utils.response_format import success_response, failure_response
from app.db.models.partner_pairing import PartnerPairing
from app.db.models.pair_badges import PairBadge
from app.db.models.badge_definition import BadgeDefinition

router = APIRouter()

@router.get("/earned-badges")
def view_earned_badges(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Find the active pair
    pair = db.query(PartnerPairing).filter(
        ((PartnerPairing.user_id == current_user.user_id) |
         (PartnerPairing.partner_id == current_user.user_id)),
        PartnerPairing.pair_status == "active"
    ).first()

    if not pair:
        return failure_response("No active pair found")

    # 2. Query all badges earned by this pair
    earned_badges = db.query(PairBadge).join(BadgeDefinition).filter(
        PairBadge.pair_id == pair.pair_id
    ).all()

    badge_list = [
        {
            "name": badge.badge.name,
            "description": badge.badge.description,
            "image_url": badge.badge.image_url,
            "badge_type": badge.badge.badge_type,
            "awarded_at": badge.awarded_at
        } for badge in earned_badges
    ]

    return success_response("Earned badges retrieved", data=badge_list)
