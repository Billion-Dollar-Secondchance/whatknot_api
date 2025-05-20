from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CreateSinglePromptRequest(BaseModel):
    prompt_text: str
    prompt_type: str  # 'emotion_checkin' or 'contextual_followup'
    emotion_tag: Optional[str] = None
    options: Optional[List[str]] = None
    allow_other: Optional[bool] = False

class SinglePromptResponse(BaseModel):
    prompt_id: str
    prompt_text: str
    prompt_type: str
    emotion_tag: Optional[str]
    options: Optional[List[str]]
    allow_other: Optional[bool]
    created_at: datetime
