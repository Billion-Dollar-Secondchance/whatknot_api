from sqlalchemy.orm import Session
from sqlalchemy import or_, and_ 
from app.crud.user import update_pairing_status
from app.db.models.partner_pairing import PartnerPairing
from fastapi import HTTPException

def get_pairing_by_user(db: Session, user_id: str) -> PartnerPairing | None:
    return (
        db.query(PartnerPairing)
          .filter(
            (PartnerPairing.user_id == user_id) |
            (PartnerPairing.partner_id == user_id)
          )
          .first()
    )


def create_pairing(db: Session, user_id: str, partner_id: str) -> PartnerPairing:
    pairing = PartnerPairing(user_id=user_id, partner_id=partner_id)
    db.add(pairing)

    # mark both as paired
    update_pairing_status(db, user_id, "paired")
    update_pairing_status(db, partner_id, "paired")

    db.commit()
    db.refresh(pairing)
    return pairing


def breakup_pairing(db: Session, user_id: str) -> None:
    pairing = (
        db.query(PartnerPairing)
        .filter(
            or_(
                PartnerPairing.user_id == user_id,
                PartnerPairing.partner_id == user_id
            )
        )
        .first()
    )

    if not pairing:
        print("❌ No active pairing found")
        raise HTTPException(status_code=400, detail="No active pairing")

    if pairing.pair_status == "broken":
        raise HTTPException(status_code=400, detail="Already broken")

    pairing.pair_status = "broken"
    db.commit()

    update_pairing_status(db, pairing.user_id, "single")
    update_pairing_status(db, pairing.partner_id, "single")

    print(f"✅ Pairing broken between: {pairing.user_id} + {pairing.partner_id}")
    