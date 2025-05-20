from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.single_vibe_prompts import SingleVibePrompt
from app.schemas.single_vibe_prompt import CreateSinglePromptRequest
from app.utils.response_format import success_response, failure_response
import json

router = APIRouter()

def generate_prompt_id(db):
    last = db.query(SingleVibePrompt).order_by(SingleVibePrompt.created_at.desc()).first()
    if last:
        try:
            num = int(last.prompt_id.split("_")[1])
        except:
            num = 0
    else:
        num = 0
    return f"vp_{num + 1:06d}"

@router.post("/single-prompts/create")
def create_single_prompt(payload: CreateSinglePromptRequest, db: Session = Depends(get_db)):
    new_id = generate_prompt_id(db)

    prompt = SingleVibePrompt(
        prompt_id=new_id,
        prompt_text=payload.prompt_text,
        prompt_type=payload.prompt_type,
        emotion_tag=payload.emotion_tag,
        options=json.dumps(payload.options) if payload.options else None,
        allow_other=str(payload.allow_other).lower()
    )
    db.add(prompt)
    db.commit()
    db.refresh(prompt)

    return success_response("Prompt created", {
        "prompt_id": prompt.prompt_id,
        "prompt_text": prompt.prompt_text,
        "prompt_type": prompt.prompt_type,
        "emotion_tag": prompt.emotion_tag,
        "options": payload.options,
        "allow_other": prompt.allow_other,
        "created_at": prompt.created_at
    })
