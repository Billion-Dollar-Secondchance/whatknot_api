from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.mystery_moodbox_questions import MysteryMoodboxQuestion, CreatedByType
from app.db.models.partner_pairing import PartnerPairing
from app.schemas.question import MoodboxQuestionCreate
from app.utils.response_format import success_response, failure_response
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/add-question")
def add_moodbox_question(
    body: MoodboxQuestionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # 1) Decide ctype as the *name* of the enum
    #    If the client sent a Python enum, .name is "USER"/"ADMIN".
    #    If they sent a string, we upper() and validate against our enum:
    if isinstance(body.created_by_type, CreatedByType):
        ctype = body.created_by_type.name
    elif body.created_by_type:
        try:
            ctype = CreatedByType[body.created_by_type.upper()].name
        except KeyError:
            raise HTTPException(400, "Invalid created_by_type")
    else:
        ctype = CreatedByType.USER.name

    # 2) Only require a pair for USER questions
    if ctype == CreatedByType.USER.name:
        pairing = db.query(PartnerPairing) \
            .filter(
                or_(
                    PartnerPairing.user_id == current_user.user_id,
                    PartnerPairing.partner_id == current_user.user_id,
                ),
                PartnerPairing.pair_status == "active",
            ) \
            .first()
        if not pairing:
            raise HTTPException(400, "You are not paired with anyone.")
        pair_id = pairing.pair_id
    else:
        pair_id = None

    q = MysteryMoodboxQuestion(
        pair_id=pair_id,
        submitted_by=current_user.user_id,
        created_by_type=ctype,              # now either "USER" or "ADMIN"
        question_type=body.question_type,   # assuming this maps similarly
        question_text=body.question_text.strip(),
        options=body.options,
        correct_answer=body.correct_answer,
    )

    try:
        db.add(q)
        db.commit()
        db.refresh(q)
        return success_response(
            message="Question added successfully.",
            data={"question_id": q.question_id},
        )
    except Exception as e:
        db.rollback()
        return failure_response(
            message="An error occurred while adding the question.",
            data=str(e),
        )
    

