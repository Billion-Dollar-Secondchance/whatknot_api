from pydantic import BaseModel
from datetime import datetime

class CreateSingleVibeRequest(BaseModel):
    name: str

class SingleVibeResponse(BaseModel):
    vibe_id: str
    name: str
    created_at: datetime
