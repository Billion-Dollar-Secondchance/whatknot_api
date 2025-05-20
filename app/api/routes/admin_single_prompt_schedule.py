from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.single_vibe_prompt_schedule import SingleVibePromptSchedule
from app.utils.response_format import success_response, failure_response
from app.schemas.single_vibe_prompt_schedule import ScheduleSinglePromptRequest

router = APIRouter()

def generate_prompt_schedule_id(db):
    # last = db.query(SingleVibePromptSchedule).order_by(SingleVibePromptSchedule.scheduled_date.desc()).first()
    last = db.query(SingleVibePromptSchedule).order_by(SingleVibePromptSchedule.prompt_schedule_id.desc()).first()
    if last:
        try:
            num = int(last.prompt_schedule_id.split("_")[1])
        except:
            num = 0
    else:
        num = 0
    return f"vps_{num + 1:06d}"

@router.post("/single-prompts/schedule")
def schedule_single_prompt(payload: ScheduleSinglePromptRequest, db: Session = Depends(get_db)):
    entry = SingleVibePromptSchedule(
        prompt_schedule_id=generate_prompt_schedule_id(db),
        prompt_id=payload.prompt_id,
        emotion_tag=payload.emotion_tag,
        scheduled_date=payload.scheduled_date
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return success_response("Prompt scheduled", {
        "prompt_schedule_id": entry.prompt_schedule_id,
        "prompt_id": entry.prompt_id,
        "emotion_tag": entry.emotion_tag,
        "scheduled_date": entry.scheduled_date
    })
