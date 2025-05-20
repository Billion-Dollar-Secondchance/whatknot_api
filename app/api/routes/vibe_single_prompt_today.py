from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.single_vibe_prompt_schedule import SingleVibePromptSchedule
from app.db.models.single_vibe_prompts import SingleVibePrompt
from app.utils.response_format import success_response
from datetime import date
import json

router = APIRouter()

@router.get("/vibe-prompts/today")
def get_today_prompts(emotion: str = Query(...), db: Session = Depends(get_db)):
    today = date.today()

    schedule_entries = db.query(SingleVibePromptSchedule).filter(
        SingleVibePromptSchedule.emotion_tag == emotion,
        SingleVibePromptSchedule.scheduled_date == today
    ).all()

    prompt_ids = [entry.prompt_id for entry in schedule_entries]

    prompts = db.query(SingleVibePrompt).filter(
        SingleVibePrompt.prompt_id.in_(prompt_ids)
    ).all()

    result = []
    for prompt in prompts:
        result.append({
            "prompt_id": prompt.prompt_id,
            "prompt_text": prompt.prompt_text,
            "prompt_type": prompt.prompt_type,
            "emotion_tag": prompt.emotion_tag,
            "options": json.loads(prompt.options) if prompt.options else [],
            "allow_other": prompt.allow_other
        })

    return success_response("Today's prompts loaded", result)
