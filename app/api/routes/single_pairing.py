# 📄 File: app/api/routes/single_pairing.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta, datetime
from app.dependencies.auth import get_current_user, get_db
from app.db.models.user import User
from app.db.models.single_vibe_pairing_prompt_status import SingleVibePairingPromptStatus
from app.db.models.single_vibe_pair_requests import SingleVibePairRequest
from app.db.models.single_vibe_paired_users import SingleVibePairedUser
from app.utils.response_format import success_response, failure_response
from app.utils.id_generator import (
    generate_pair_request_id,
    generate_final_pair_id
)
from pydantic import BaseModel

router = APIRouter()

# ✅ 1. Get eligible pairings
@router.get("/single/pairing/eligible")
def get_eligible_pairings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()

    eligible_pairs = db.query(SingleVibePairingPromptStatus).filter(
        ((SingleVibePairingPromptStatus.user_1_id == current_user.user_id) |
         (SingleVibePairingPromptStatus.user_2_id == current_user.user_id)),
        SingleVibePairingPromptStatus.match_count >= 5,
        SingleVibePairingPromptStatus.last_matched_on >= today - timedelta(days=7),
        SingleVibePairingPromptStatus.prompted == False,
        SingleVibePairingPromptStatus.active == True
    ).all()

    response = []
    for p in eligible_pairs:
        partner_id = p.user_2_id if p.user_1_id == current_user.user_id else p.user_1_id
        partner = db.query(User).filter_by(user_id=partner_id).first()
        if partner:
            response.append({
                "user_id": partner.user_id,
                "name": partner.name,
                "profile_image": partner.profile_image,
                "match_count": p.match_count,
                "last_matched_on": p.last_matched_on
            })

    return success_response("Eligible pairing suggestions", response)

# ✅ 2. Send pairing request
class PairRequest(BaseModel):
    receiver_id: str

@router.post("/single/pairing/request")
def send_pair_request(
    payload: PairRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    users = sorted([current_user.user_id, payload.receiver_id])
    status = db.query(SingleVibePairingPromptStatus).filter_by(
        user_1_id=users[0], user_2_id=users[1]
    ).first()

    if not status or status.match_count < 5:
        return failure_response("Not eligible for pairing request")

    existing = db.query(SingleVibePairRequest).filter_by(
        sender_id=current_user.user_id,
        receiver_id=payload.receiver_id,
        status="pending"
    ).first()

    if existing:
        return failure_response("Request already sent")

    request = SingleVibePairRequest(
        request_id=generate_pair_request_id(db),
        sender_id=current_user.user_id,
        receiver_id=payload.receiver_id,
        match_count=status.match_count,
        requested_on=datetime.utcnow(),
        status="pending"
    )
    status.prompted = True

    db.add(request)
    db.commit()
    return success_response("Pair request sent")

# ✅ 3. Respond to pairing request
class PairResponse(BaseModel):
    request_id: str
    accept: bool

@router.post("/single/pairing/respond")
def respond_to_pair_request(
    payload: PairResponse,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    request = db.query(SingleVibePairRequest).filter_by(request_id=payload.request_id).first()

    if not request or request.status != "pending":
        return failure_response("Invalid or already handled request")

    if payload.accept:
        pair = SingleVibePairedUser(
            pair_id=generate_final_pair_id(db),
            user_1_id=request.sender_id,
            user_2_id=request.receiver_id,
            paired_on=datetime.utcnow()
        )
        db.add(pair)
        request.status = "accepted"

        db.query(SingleVibePairRequest).filter(
            SingleVibePairRequest.status == "pending",
            ((SingleVibePairRequest.sender_id.in_([request.sender_id, request.receiver_id])) |
             (SingleVibePairRequest.receiver_id.in_([request.sender_id, request.receiver_id])))
        ).update({SingleVibePairRequest.status: "expired"}, synchronize_session=False)
    else:
        request.status = "rejected"

    db.commit()
    return success_response("Request response recorded")

@router.get("/pairing/request-preview/{receiver_id}")
def get_pair_request_preview(
    receiver_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if they've matched enough times
    users = sorted([current_user.user_id, receiver_id])
    status = db.query(SingleVibePairingPromptStatus).filter_by(
        user_1_id=users[0], user_2_id=users[1]
    ).first()

    if not status or status.match_count < 5:
        return failure_response("You’re not eligible to pair with this user yet")

    # Get the other user's public profile
    other = db.query(User).filter_by(user_id=receiver_id).first()

    if not other:
        return failure_response("User not found")

    shared_vibes = []
    if current_user.vibe_keywords and other.vibe_keywords:
        shared_vibes = list(set(current_user.vibe_keywords.split(",")) & set(other.vibe_keywords.split(",")))

    profile = {
        "user_id": other.user_id,
        "name": other.name,
        "profile_image": other.profile_image,
        "location": other.location,
        "education": other.education,
        "vibe_keywords": other.vibe_keywords.split(",") if other.vibe_keywords else [],
        "shared_vibes": shared_vibes,
        "match_count": status.match_count
    }

    return success_response("Pair preview fetched", profile)

