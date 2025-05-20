from pydantic import BaseModel
from datetime import date

class ScheduleSingleVibeRequest(BaseModel):
    vibe_id: str
    scheduled_date: date
