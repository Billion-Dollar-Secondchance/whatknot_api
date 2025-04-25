from pydantic import BaseModel, EmailStr, field_serializer
from typing import Optional, Literal, Union, Any
from datetime import datetime,date
import pytz

IST = pytz.timezone("Asia/Kolkata")

class UserResponse(BaseModel):
    
    user_id: str
    email: Optional[EmailStr] = None
    login_type: str
    name: Optional[str] = None
    profile_image: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    google_id: Optional[str] = None
    vibe_as: Optional[str] = None
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True  
    }

    @field_serializer("created_at")
    def format_created_at(self, v: datetime, info) -> str:
        ist_dt = v.astimezone(IST)
        return ist_dt.strftime("%d-%m-%Y %I:%M:%S %p IST")

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class UserCreate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    login_type: str  # 'email', 'google', or 'guest'
    vibe_as: Optional[str] = None
    guest_token: Optional[str] = None
    name: Optional[str] = None

class UserOut(BaseModel):
    user_id: str
    email: Optional[EmailStr] = None
    login_type: str
    vibe_as: Optional[str] = None
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True  # v2’s replacement for orm_mode
    }

    @field_serializer("created_at")
    def format_created_at(self, v: datetime, info) -> str:
        ist_dt = v.astimezone(IST)
        return ist_dt.strftime("%d-%m-%Y %I:%M:%S %p IST")

class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    profile_image: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    vibe_as: Optional[str] = None  # ← Add this

class WrappedResponse(BaseModel):
    status: Literal["success", "failure"]
    message: str
    data: Optional[Any] = None
    # data: Optional[LoginResponse] = None

class UpdateUserSchema(BaseModel):
    name: Optional[str]
    profile_image: Optional[str]
    gender: Optional[str]
    date_of_birth: Optional[date]
    vibe_as: Optional[str]

    class Config:
        orm_mode = True