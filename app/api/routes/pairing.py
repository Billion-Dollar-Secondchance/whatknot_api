# from fastapi import APIRouter, Depends, status
# from pydantic import BaseModel
# from fastapi.responses import JSONResponse
# from sqlalchemy.orm import Session
# from app.services.pairing import (
#     join_partner_by_code,
#     get_my_partner,
#     breakup_pairing,
# )
# from app.dependencies.auth import get_current_user, get_db
# from app.schemas.pairing import PairingRequest, WrappedPairingResponse, PairingResponse
# from app.schemas.user import UserResponse
# from app.db.models.user import User


# # router = APIRouter(prefix="/pairing", tags=["Pairing"])
# router = APIRouter()
# @router.post("/join", response_model=WrappedPairingResponse)
# def join_pairing(
#     payload: PairingRequest,
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user),
# ):
#     pairing = join_partner_by_code(db, current_user.user_id, payload.pairing_code)
#     partner = get_my_partner(db, current_user.user_id)

#     if not partner:
#         return WrappedPairingResponse(
#             status="failure",
#             message="No active pairing found",
#             data=None
#         )

#     return WrappedPairingResponse(
#         status="success",
#         message="Paired successfully",
#         data=PairingResponse(partner=UserResponse.model_validate(partner))
#     )


# # @router.post("/join", response_model=WrappedPairingResponse)
# # def join_pairing(
# #     payload: PairingRequest,
# #     db: Session = Depends(get_db),
# #     current_user=Depends(get_current_user),
# # ):
# #     pairing = join_partner_by_code(db, current_user.user_id, payload.pairing_code)
# #     partner = get_my_partner(db, current_user.user_id)
# #     return WrappedPairingResponse(
# #         status="success",
# #         message="Paired successfully",
# #         data=PairingResponse(partner=UserResponse.model_validate(partner))
# #     )

# class BreakupRequest(BaseModel):
#     user_id: str


# @router.post("/breakup")
# def breakup_pairing_route(request: BreakupRequest, db: Session = Depends(get_db)):
#     result = breakup_pairing(db, request.user_id)
#     return result

# @router.get("/me", response_model=WrappedPairingResponse)
# def get_pairing(
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user),
# ):
#     partner = get_my_partner(db, current_user.user_id)
#     if not partner:
#         return WrappedPairingResponse(
#             status="failure",
#             message="No partner paired yet",
#             data=None
#         )
#     return WrappedPairingResponse(
#         status="success",
#         message="Partner fetched",
#         data=PairingResponse(partner=UserResponse.model_validate(partner))
#     )

# app/api/routes/pairing.py
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.schemas.pairing import (
    PairingRequest, BreakupRequest,
    WrappedPairingResponse, PairingResponse
)
from app.schemas.user import UserResponse
from app.services.pairing import join_partner_by_code, break_up_partner, get_my_partner
from app.dependencies.auth import get_current_user, get_db
from app.db.models.user import User

router = APIRouter()

@router.post("/join", response_model=WrappedPairingResponse)
def join_pairing(
    payload: PairingRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        partner = join_partner_by_code(db, current_user.user_id, payload.pairing_code)
        return WrappedPairingResponse(
            status="success",
            message="Paired successfully",
            data=PairingResponse(partner=UserResponse.from_orm(partner))
        )
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"status": "failure", "message": e.detail, "data": None}
        )


@router.post("/breakup", response_model=WrappedPairingResponse)
def breakup_pairing(
    payload: BreakupRequest,
    db: Session = Depends(get_db),
):
    try:
        break_up_partner(db, payload.user_id)
        return WrappedPairingResponse(
            status="success",
            message="Breakup successful",
            data=None
        )
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"status": "failure", "message": e.detail, "data": None}
        )
