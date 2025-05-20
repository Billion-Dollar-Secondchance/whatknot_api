from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.single_vibe_schedule import SingleVibeSchedule
from app.db.models.single_vibe_definition import SingleVibeDefinition
from app.schemas.single_vibe_schedule import ScheduleSingleVibeRequest
from app.utils.id_generator import generate_single_vibe_schedule_id
from app.utils.response_format import success_response, failure_response

router = APIRouter()

@router.post("/admin/single-vibes/schedule")
def schedule_single_vibe(
    payload: ScheduleSingleVibeRequest,
    db: Session = Depends(get_db)
):
    # Check vibe exists
    vibe = db.query(SingleVibeDefinition).filter(SingleVibeDefinition.vibe_id == payload.vibe_id).first()
    if not vibe:
        return failure_response("Vibe ID not found")

    # Prevent duplicate schedule
    existing = db.query(SingleVibeSchedule).filter(
        SingleVibeSchedule.vibe_id == payload.vibe_id,
        SingleVibeSchedule.scheduled_date == payload.scheduled_date
    ).first()
    if existing:
        return failure_response("Vibe already scheduled for this date")

    schedule_id = generate_single_vibe_schedule_id(db)

    entry = SingleVibeSchedule(
        schedule_id=schedule_id,
        vibe_id=payload.vibe_id,
        scheduled_date=payload.scheduled_date
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return success_response("Vibe scheduled", {
        "schedule_id": entry.schedule_id,
        "vibe_id": entry.vibe_id,
        "scheduled_date": entry.scheduled_date
    })
