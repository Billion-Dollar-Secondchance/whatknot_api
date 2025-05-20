# app/api/routes/single_vibe_prompt_response.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
from app.db.session import get_db
from app.db.models.single_vibe_prompt_response import SingleVibePromptResponse
from app.utils.response_format import success_response, failure_response
from app.dependencies.auth import get_current_user
from app.db.models.user import User
from app.schemas.single_vibe_prompt_response import SubmitSingleVibeAnswerRequest

router = APIRouter()

def generate_response_id(db):
    last = db.query(SingleVibePromptResponse).order_by(SingleVibePromptResponse.submitted_at.desc()).first()
    if last:
        try:
            num = int(last.vibe_response_id.split("_")[1])
        except:
            num = 0
    else:
        num = 0
    return f"svr_{num + 1:06d}"

@router.post("/single-vibe/submit")
def submit_single_prompt_response(
    payload: SubmitSingleVibeAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.query(SingleVibePromptResponse).filter_by(
        user_id=current_user.user_id,
        prompt_schedule_id=payload.prompt_schedule_id
    ).first()

    if existing:
        return failure_response("Response already submitted for this prompt", status_code=400)

    response = SingleVibePromptResponse(
        vibe_response_id=generate_response_id(db),
        user_id=current_user.user_id,
        prompt_id=payload.prompt_id,
        prompt_schedule_id=payload.prompt_schedule_id,
        answer=payload.answer.strip(),
        submitted_at=datetime.utcnow()
    )
    db.add(response)
    db.commit()
    return success_response("Response submitted successfully")
