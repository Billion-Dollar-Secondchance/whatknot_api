# app/api/routes/streak.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.auth import get_db, get_current_user
from app.db.models.partner_pairing import PartnerPairing
from app.db.models.pair_streak import PairStreak
from app.db.models.user import User
from app.utils.response_format import success_response, failure_response

router = APIRouter()

@router.get("/streak")
def get_pair_streak(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Find active pair
    pair = db.query(PartnerPairing).filter(
        ((PartnerPairing.user_id == current_user.user_id) |
         (PartnerPairing.partner_id == current_user.user_id)),
        PartnerPairing.pair_status == "active"
    ).first()

    if not pair:
        return failure_response("No active pair found")

    # Fetch streak data
    streak = db.query(PairStreak).filter(PairStreak.pair_id == pair.pair_id).first()

    if not streak:
        return success_response("No streak found yet", {
            "current_streak": 0,
            "longest_streak": 0,
            "streak_icon_url": "https://i.pinimg.com/736x/8a/70/9a/8a709a337d69d05f1239690195ec09cb.jpg"
        })

    return success_response("Streak fetched successfully", {
        "current_streak": streak.current_streak,
        "longest_streak": streak.longest_streak,
        "streak_icon_url": "https://i.pinimg.com/736x/8a/70/9a/8a709a337d69d05f1239690195ec09cb.jpg"
    })
