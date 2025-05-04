# app/services/pairing.py
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from datetime import datetime

from app.db.models.partner_pairing import PartnerPairing
from app.db.models.user import User
from app.crud.user import update_pairing_status

def join_partner_by_code(db: Session, user_id: str, pairing_code: str) -> User:
    you = db.query(User).get(user_id)
    partner = db.query(User).filter(User.pairing_code == pairing_code).first()

    if not you or not partner:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User or partner not found")
    if you.user_id == partner.user_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Cannot pair with yourself")

    # any active pairing?
    existing = db.query(PartnerPairing).filter(
        or_(
            PartnerPairing.user_id == you.user_id,
            PartnerPairing.partner_id == you.user_id,
            PartnerPairing.user_id == partner.user_id,
            PartnerPairing.partner_id == partner.user_id,
        ),
        PartnerPairing.pair_status == "active"
    ).first()
    if existing:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "One of the users is already paired")

    new_pair = PartnerPairing(
        user_id=you.user_id,
        partner_id=partner.user_id,
        pair_status="active",
        created_at=datetime.utcnow()
    )
    db.add(new_pair)
    you.pairing_status = "paired"
    partner.pairing_status = "paired"
    db.commit()
    return partner


def break_up_partner(db: Session, user_id: str) -> None:
    pair = db.query(PartnerPairing).filter(
        or_(
            PartnerPairing.user_id == user_id,
            PartnerPairing.partner_id == user_id
        ),
        PartnerPairing.pair_status == "active"
    ).first()
    if not pair:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No active pairing found")

    pair.pair_status = "broken"
    # update both users
    you = db.query(User).get(pair.user_id)
    them = db.query(User).get(pair.partner_id)
    you.pairing_status = "not_paired"
    them.pairing_status = "not_paired"

    db.commit()
    
def get_my_partner(db: Session, user_id: str) -> User | None:
    pairing = (
        db.query(PartnerPairing)
          .filter(
             ((PartnerPairing.user_id == user_id) | (PartnerPairing.partner_id == user_id)),
             PartnerPairing.pair_status == "active"
          )
          .first()
    )
    if not pairing:
        return None

    partner_id = pairing.partner_id if pairing.user_id == user_id else pairing.user_id
    return db.query(User).filter(User.user_id == partner_id).first()