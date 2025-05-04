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
