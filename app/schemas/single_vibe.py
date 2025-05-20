from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SingleVibeSubmitRequest(BaseModel):
    vibe: str
    prompt_answers: Optional[List[str]] = []

class SingleVibeResponse(BaseModel):
    single_vibe_id: str
    user_id: str
    vibe: str
    prompt_answers: Optional[List[str]]
    answer_status: str
    created_at: datetime
