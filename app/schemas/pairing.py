# app/schemas/pairing.py
from pydantic import BaseModel
from typing import Optional, Literal, Union, Any
from app.schemas.user import UserResponse

class PairingRequest(BaseModel):
    pairing_code: str  # the 6‑digit partner code

class PairingResponse(BaseModel):
    partner: Optional[UserResponse]


class BreakupRequest(BaseModel):
    user_id: str 
    partner_code: str

class WrappedPairingResponse(BaseModel):
    status: Literal["success", "failure"]
    message: str
    data: Optional[PairingResponse] = None

