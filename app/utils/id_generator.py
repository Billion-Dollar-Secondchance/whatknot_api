from sqlalchemy.orm import Session
from app.db.models.single_vibe_entry import SingleVibeEntry
from app.db.models.single_vibe_schedule import SingleVibeSchedule
from app.db.models.single_vibe_matched_pairs import SingleVibeMatchedPair
from app.db.models.single_vibe_pairing_prompt_status import SingleVibePairingPromptStatus
from app.db.models.user_relationship_settings import UserRelationshipSettings
from app.db.models.single_vibe_pair_requests import SingleVibePairRequest
from app.db.models.single_vibe_paired_users import SingleVibePairedUser


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

def generate_single_vibe_match_id(db: Session) -> str:
    last_match = (
        db.query(SingleVibeMatchedPair)
        .order_by(SingleVibeMatchedPair.matched_on.desc())
        .first()
    )
    if last_match:
        try:
            last_num = int(last_match.single_vibe_match_id.split("_")[1])
        except (IndexError, ValueError):
            last_num = 0
    else:
        last_num = 0

    return f"svm_{last_num + 1:06d}"


def generate_pairing_prompt_id(db: Session):
    last = db.query(SingleVibePairingPromptStatus).order_by(SingleVibePairingPromptStatus.last_matched_on.desc()).first()
    if last:
        try:
            num = int(last.pairing_prompt_id.split("_")[1])
        except:
            num = 0
    else:
        num = 0
    return f"svp_{num + 1:06d}"


def generate_relationship_settings_id(db):
    last = db.query(UserRelationshipSettings).order_by(UserRelationshipSettings.updated_at.desc()).first()
    if last:
        try:
            num = int(last.settings_id.split("_")[1])
        except:
            num = 0
    else:
        num = 0
    return f"urs_{num + 1:06d}"


def generate_pair_request_id(db: Session) -> str:
    last_request = (
        db.query(SingleVibePairRequest)
        .order_by(SingleVibePairRequest.requested_on.desc())
        .first()
    )
    if last_request:
        try:
            last_num = int(last_request.request_id.split("_")[1])
        except (IndexError, ValueError):
            last_num = 0
    else:
        last_num = 0

    return f"spr_{last_num + 1:06d}"


def generate_final_pair_id(db: Session) -> str:
    last_pair = (
        db.query(SingleVibePairedUser)
        .order_by(SingleVibePairedUser.paired_on.desc())
        .first()
    )
    if last_pair:
        try:
            last_num = int(last_pair.pair_id.split("_")[1])
        except (IndexError, ValueError):
            last_num = 0
    else:
        last_num = 0

    return f"spu_{last_num + 1:06d}"