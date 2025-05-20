from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.auth import get_current_user
from app.db.models.single_vibe_entry import SingleVibeEntry
from app.schemas.single_vibe import SingleVibeSubmitRequest, SingleVibeResponse
from app.utils.response_format import success_response, failure_response
from app.utils.id_generator import generate_single_vibe_id
import json

router = APIRouter()

@router.post("/vibe-match/singles/submit")
def submit_single_vibe(
    payload: SingleVibeSubmitRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Ensure the user is vibing as a single
    if current_user.vibe_as != "single":
        return failure_response("Only singles can submit this vibe.")

    if not current_user.interested_in:
        return failure_response("Please update your 'interested_in' preference in your profile.")

    # Check if user has already submitted today
    from datetime import datetime
    today = datetime.utcnow().date()
    existing_entry = db.query(SingleVibeEntry).filter(
        SingleVibeEntry.user_id == current_user.user_id,
        SingleVibeEntry.created_at >= datetime.combine(today, datetime.min.time()),
        SingleVibeEntry.created_at <= datetime.combine(today, datetime.max.time())
    ).first()

    if existing_entry:
        return failure_response("You’ve already submitted your vibe for today.")

    # Generate new ID
    new_id = generate_single_vibe_id(db)

    # Determine answer status
    answer_status = "complete" if payload.prompt_answers and len(payload.prompt_answers) >= 2 else "incomplete"

    new_entry = SingleVibeEntry(
        single_vibe_id=new_id,
        user_id=current_user.user_id,
        vibe=payload.vibe,
        prompt_answers=json.dumps(payload.prompt_answers),  # store as string
        answer_status=answer_status
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return success_response(
        "Vibe submitted successfully",
        {
            "single_vibe_id": new_entry.single_vibe_id,
            "vibe": new_entry.vibe,
            "answer_status": new_entry.answer_status,
            "created_at": new_entry.created_at,
            "user_id": new_entry.user_id,
            "prompt_answers": payload.prompt_answers
        }
    )
