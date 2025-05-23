from sqlalchemy.orm import Session
from app.db.models.single_vibe_pair_requests import SingleVibePairRequest
from app.utils.id_generator import generate_pair_request_id
from datetime import datetime
from app.db.models.single_vibe_paired_users import SingleVibePairedUser
from app.utils.id_generator import generate_final_pair_id


def send_pair_request(db: Session, sender_id: str, receiver_id: str, match_count: int):
    # Check for existing active request
    existing = db.query(SingleVibePairRequest).filter_by(
        sender_id=sender_id, receiver_id=receiver_id, status="pending"
    ).first()

    if existing:
        return {"error": "Request already sent"}

    request = SingleVibePairRequest(
        request_id=generate_pair_request_id(db),
        sender_id=sender_id,
        receiver_id=receiver_id,
        match_count=match_count,
        requested_on=datetime.utcnow(),
        status="pending"
    )
    db.add(request)
    db.commit()
    return {"message": "Pair request sent"}


def respond_to_pair_request(db: Session, request_id: str, accepted: bool):
    request = db.query(SingleVibePairRequest).filter_by(request_id=request_id).first()

    if not request or request.status != "pending":
        return {"error": "Invalid or already handled request"}

    if accepted:
        # ✅ Create final pair
        final_pair = SingleVibePairedUser(
            pair_id=generate_final_pair_id(db),
            user_1_id=request.sender_id,
            user_2_id=request.receiver_id,
            paired_on=datetime.utcnow()
        )
        db.add(final_pair)

        # ❌ Expire other active requests involving sender/receiver
        db.query(SingleVibePairRequest).filter(
            SingleVibePairRequest.status == "pending",
            ((SingleVibePairRequest.sender_id == request.sender_id) | (SingleVibePairRequest.receiver_id == request.sender_id) |
             (SingleVibePairRequest.sender_id == request.receiver_id) | (SingleVibePairRequest.receiver_id == request.receiver_id))
        ).update({SingleVibePairRequest.status: "expired"}, synchronize_session=False)

        request.status = "accepted"
    else:
        request.status = "rejected"

    db.commit()
    return {"message": f"Request {'accepted' if accepted else 'rejected'}"}
