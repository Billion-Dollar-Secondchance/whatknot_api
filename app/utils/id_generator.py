from sqlalchemy.orm import Session
from app.db.models.single_vibe_entry import SingleVibeEntry
from app.db.models.single_vibe_schedule import SingleVibeSchedule


def generate_single_vibe_id(db: Session) -> str:
    last_entry = (
        db.query(SingleVibeEntry)
        .order_by(SingleVibeEntry.created_at.desc())
        .first()
    )
    if last_entry:
        try:
            last_num = int(last_entry.single_vibe_id.split("_")[1])
        except (IndexError, ValueError):
            last_num = 0
    else:
        last_num = 0

    return f"sv_{last_num + 1:06d}"


def generate_single_vibe_schedule_id(db):
    last = db.query(SingleVibeSchedule).order_by(SingleVibeSchedule.scheduled_date.desc()).first()
    if last:
        try:
            num = int(last.schedule_id.split("_")[1])
        except:
            num = 0
    else:
        num = 0
    return f"vs_{num + 1:06d}"
