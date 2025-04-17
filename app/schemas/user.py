from pydantic import BaseModel, EmailStr
# from pydantic_settings import BaseModel, EmailStr 

from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    login_type: str
    vibe_as: str

class UserOut(BaseModel):
    user_id: str
    email: EmailStr
    vibe_as: str
    created_at: datetime

    class Config:
        orm_mode = True
