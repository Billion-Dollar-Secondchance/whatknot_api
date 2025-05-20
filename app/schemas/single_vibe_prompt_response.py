# app/schemas/single_vibe_prompt_response.py
from pydantic import BaseModel
from uuid import UUID
from datetime import date

class SubmitSingleVibeAnswerRequest(BaseModel):
    prompt_schedule_id: str
    prompt_id: str
    answer: str
