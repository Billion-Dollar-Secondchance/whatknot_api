from pydantic import BaseModel
from datetime import date

class ScheduleSinglePromptRequest(BaseModel):
    prompt_id: str
    # vibe_id: str
    emotion_tag: str
    scheduled_date: date
