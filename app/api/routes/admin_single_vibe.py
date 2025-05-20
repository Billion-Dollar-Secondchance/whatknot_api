from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.single_vibe_definition import SingleVibeDefinition
from app.schemas.single_vibe_definition import CreateSingleVibeRequest, SingleVibeResponse
from app.utils.response_format import success_response, failure_response

router = APIRouter()

def generate_single_vibe_id(db: Session) -> str:
    last_entry = db.query(SingleVibeDefinition).order_by(SingleVibeDefinition.created_at.desc()).first()
    if last_entry:
        try:
            last_num = int(last_entry.vibe_id.split("_")[1])
        except (IndexError, ValueError):
            last_num = 0
    else:
        last_num = 0
    return f"vb_{last_num + 1:06d}"

@router.post("/single-vibes/create")
def create_single_vibe(
    payload: CreateSingleVibeRequest,
    db: Session = Depends(get_db)
):
    existing = db.query(SingleVibeDefinition).filter(SingleVibeDefinition.name.ilike(payload.name)).first()
    if existing:
        return failure_response("Vibe name already exists")

    new_id = generate_single_vibe_id(db)
    vibe = SingleVibeDefinition(
        vibe_id=new_id,
        name=payload.name
    )
    db.add(vibe)
    db.commit()
    db.refresh(vibe)

    return success_response("Vibe created successfully", {
        "vibe_id": vibe.vibe_id,
        "name": vibe.name,
        "created_at": vibe.created_at
    })
