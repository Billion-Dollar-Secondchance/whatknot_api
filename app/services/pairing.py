# from sqlalchemy.orm import Session
# from sqlalchemy import or_
# from datetime import datetime
# from app.crud.user import get_user_by_id
# from app.db.models.partner_pairing import PartnerPairing
# from app.db.models.user import User
# from app.crud.pairing import get_pairing_by_user


# def join_partner_by_code(db: Session, user_id: str, pairing_code: str):
#     user = db.query(User).filter(User.user_id == user_id).first()
#     partner = db.query(User).filter(User.pairing_code == pairing_code).first()

#     if not user or not partner:
#         return {"status": "failure", "message": "User or partner not found", "data": None}

#     if user.user_id == partner.user_id:
#         return {"status": "failure", "message": "Cannot pair with yourself", "data": None}

#     # Check if either user is already in an active pair
#     existing_pair = db.query(PartnerPairing).filter(
#         or_(
#             PartnerPairing.user_id == user.user_id,
#             PartnerPairing.partner_id == user.user_id,
#             PartnerPairing.user_id == partner.user_id,
#             PartnerPairing.partner_id == partner.user_id
#         ),
#         PartnerPairing.pair_status == 'active'  # Check for active pairing
#     ).first()

#     if existing_pair:
#         return {"status": "failure", "message": "One of the users is already paired", "data": None}

#     # If there is a broken pairing, update the status and create a new pairing
#     broken_pair = db.query(PartnerPairing).filter(
#         or_(
#             PartnerPairing.user_id == user.user_id,
#             PartnerPairing.partner_id == user.user_id,
#             PartnerPairing.user_id == partner.user_id,
#             PartnerPairing.partner_id == partner.user_id
#         ),
#         PartnerPairing.pair_status == 'broken'  # Check for broken pairings
#     ).first()

#     if broken_pair:
#         broken_pair.pair_status = 'active'  # Update the broken pair status to 'active'

#     # Create the new pairing
#     new_pair = PartnerPairing(
#         user_id=user.user_id,
#         partner_id=partner.user_id,
#         pair_status='active',  # New active pairing
#         created_at=datetime.utcnow()
#     )

#     db.add(new_pair)
#     db.commit()

#     # Update the user pairing status to active
#     user.pairing_status = 'active'
#     partner.pairing_status = 'active'

#     db.commit()

#     return {
#         "status": "success",
#         "message": "Paired successfully",
#         "data": {
#             "pair_id": new_pair.pair_id
#         }
#     }

# # def breakup_pairing(db: Session, user_id: str):
# #     pair = db.query(PartnerPairing).filter(
# #         or_(
# #             PartnerPairing.user_id == user_id,
# #             PartnerPairing.partner_id == user_id
# #         ),
# #         PartnerPairing.pair_status == 'paired'
# #     ).first()

# #     if not pair:
# #         return {"status": "failure", "message": "No active pairing found", "data": None}

# #     pair.pair_status = 'broken'

# #     # Update pairing_status on both users
# #     user = db.query(User).filter(User.user_id == pair.user_id).first()
# #     partner = db.query(User).filter(User.user_id == pair.partner_id).first()

# #     if user:
# #         user.pairing_status = 'not_paired'
# #     if partner:
# #         partner.pairing_status = 'not_paired'

# #     db.commit()

# #     return {
# #         "status": "success",
# #         "message": "Pairing broken successfully",
# #         "data": {
# #             "pair_id": pair.pair_id
# #         }
# #     }

# def breakup_pairing(db: Session, user_id: str):
#     pair = db.query(PartnerPairing).filter(
#         or_(
#             PartnerPairing.user_id == user_id,
#             PartnerPairing.partner_id == user_id
#         ),
#         PartnerPairing.pair_status == 'active'  # Only allow breakup if the pairing is active
#     ).first()

#     if not pair:
#         return {"status": "failure", "message": "No active pairing found", "data": None}

#     pair.pair_status = 'broken'

#     # Update pairing_status on both users
#     user = db.query(User).filter(User.user_id == pair.user_id).first()
#     partner = db.query(User).filter(User.user_id == pair.partner_id).first()

#     if user:
#         user.pairing_status = 'not_paired'
#     if partner:
#         partner.pairing_status = 'not_paired'

#     db.commit()

#     return {
#         "status": "success",
#         "message": "Pairing broken successfully",
#         "data": {
#             "pair_id": pair.pair_id
#         }
#     }


# def get_my_partner(db: Session, user_id: str):
#     # First, try to get an active pairing for the user
#     pairing = (
#         db.query(PartnerPairing)
#         .filter(
#             ((PartnerPairing.user_id == user_id) | (PartnerPairing.partner_id == user_id)),
#             PartnerPairing.pair_status == "active"  # Only look for active pairings first
#         )
#         .first()
#     )

#     if pairing:
#         # If an active pairing is found, return the partner info
#         partner_id = pairing.partner_id if pairing.user_id == user_id else pairing.user_id
#         return db.query(User).filter(User.user_id == partner_id).first()

#     # If no active pairing is found, check for a broken pairing
#     pairing = (
#         db.query(PartnerPairing)
#         .filter(
#             ((PartnerPairing.user_id == user_id) | (PartnerPairing.partner_id == user_id)),
#             PartnerPairing.pair_status == "broken"  # Look for broken pairings
#         )
#         .first()
#     )

#     if pairing:
#         # If a broken pairing exists, return a message that a new pairing can be created
#         partner_id = pairing.partner_id if pairing.user_id == user_id else pairing.user_id
#         return {
#             "status": "failure",
#             "message": "The pairing was previously broken. Please create a new pairing.",
#             "data": {
#                 "partner_id": partner_id
#             }
#         }

#     # If no pairing exists, return None or a suitable message
#     return {
#         "status": "failure",
#         "message": "No active or broken pairing found.",
#         "data": None
#     }



# # def get_my_partner(db: Session, current_user_id: str):
# #     pairing = get_pairing_by_user(db, current_user_id)

# #     if not pairing or pairing.pair_status == "broken":
# #         return {
# #             "status": "failure",
# #             "message": "No active pairing found",
# #             "data": None
# #         }

# #     other_id = pairing.partner_id if pairing.user_id == current_user_id else pairing.user_id
# #     partner = get_user_by_id(db, other_id)

# #     return {
# #         "status": "success",
# #         "message": "Active partner found",
# #         "data": {
# #             "partner": {
# #                 "user_id": partner.user_id,
# #                 "name": partner.name,
# #                 "email": partner.email,
# #                 "profile_image": partner.profile_image,
# #                 "gender": partner.gender,
# #                 "date_of_birth": partner.date_of_birth
# #             }
# #         }
# #     }

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