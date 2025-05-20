from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.single_vibe_prompt_schedule import SingleVibePromptSchedule
from app.db.models.single_vibe_prompts import SingleVibePrompt
from app.utils.response_format import success_response
import json
from datetime import date

router = APIRouter()

@router.get("/vibe-prompts/today")
def get_today_prompts(vibe_id: str = Query(...), db: Session = Depends(get_db)):
    today = date.today()

    schedules = db.query(SingleVibePromptSchedule).filter(
        SingleVibePromptSchedule.vibe_id == vibe_id,
        SingleVibePromptSchedule.scheduled_date == today
    ).all()

    prompt_ids = [s.prompt_id for s in schedules]
    prompts = db.query(SingleVibePrompt).filter(SingleVibePrompt.prompt_id.in_(prompt_ids)).all()

    data = [{
        "prompt_id": p.prompt_id,
        "prompt_text": p.prompt_text,
        "prompt_type": p.prompt_type,
        "emotion_tag": p.emotion_tag,
        "options": json.loads(p.options) if p.options else [],
        "allow_other": p.allow_other
    } for p in prompts]

    return success_response("Today's prompts loaded", data)
