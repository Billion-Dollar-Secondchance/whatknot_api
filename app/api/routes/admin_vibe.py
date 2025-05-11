# File: app/api/routes/admin_vibe.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from typing import List
from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.db.models.user import User
from app.db.models.vibe_match import VibeQuestion, VibeQuestionDayMapping, VibeQuestionDateMapping
from app.schemas.vibe_question import VibeQuestionCreate, VibeQuestionUpdate, VibeDayMappingBulkCreate, VibeDateMappingBulkCreate
from app.utils.response_format import success_response, failure_response

router = APIRouter()

@router.post("/vibe-question/add")
def admin_add_vibe_question(
    payload: VibeQuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_question = VibeQuestion(
        question_id=uuid4(),
        question_text=payload.question_text,
        question_type=payload.question_type,
        options=payload.options,
        is_active=True
    )
    db.add(new_question)
    db.commit()

    return success_response(message="Question created", data={"question_id": str(new_question.question_id)})


@router.get("/vibe-questions")
def get_all_vibe_questions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    questions = db.query(VibeQuestion).order_by(VibeQuestion.created_at.desc()).all()
    return success_response(
        message="Questions fetched",
        data=[
            {
                "question_id": str(q.question_id),
                "question_text": q.question_text,
                "question_type": q.question_type,
                "options": q.options,
                "is_active": q.is_active
            }
            for q in questions
        ]
    )


@router.patch("/vibe-question/{question_id}")
def update_vibe_question(
    question_id: UUID,
    payload: VibeQuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    question = db.query(VibeQuestion).filter_by(question_id=question_id).first()
    if not question:
        return failure_response("Question not found", status_code=404)

    if payload.question_text is not None:
        question.question_text = payload.question_text
    if payload.question_type is not None:
        question.question_type = payload.question_type
    if payload.options is not None:
        if not isinstance(payload.options, dict):
            return failure_response("Options must be a dictionary", status_code=400)
        question.options = payload.options
    if payload.is_active is not None:
        question.is_active = payload.is_active

    db.commit()
    return success_response(message="Question updated")


@router.delete("/vibe-question/{question_id}")
def soft_delete_vibe_question(
    question_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    question = db.query(VibeQuestion).filter_by(question_id=question_id).first()
    if not question:
        return failure_response("Question not found", status_code=404)

    question.is_active = False
    db.commit()
    return success_response(message="Question deactivated")


@router.post("/vibe-question/day-mapping")
def bulk_map_questions_to_days_or_date(
    payload: VibeDayMappingBulkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_questions = db.query(VibeQuestion).filter(VibeQuestion.question_id.in_(payload.question_ids)).all()
    if len(existing_questions) != len(payload.question_ids):
        return failure_response("Some question_ids are invalid", status_code=400)

    mappings = []

    if payload.days_condition:
        mappings.extend([
            VibeQuestionDayMapping(
                mapping_id=uuid4(),
                question_id=qid,
                days_condition=payload.days_condition
            ) for qid in payload.question_ids
        ])

    if payload.scheduled_date:
        mappings.extend([
            VibeQuestionDateMapping(
                mapping_id=uuid4(),
                question_id=qid,
                scheduled_date=payload.scheduled_date
            ) for qid in payload.question_ids
        ])

    if not mappings:
        return failure_response("Either days_condition or scheduled_date must be provided", status_code=400)

    db.add_all(mappings)
    db.commit()

    return success_response(message="Mappings created", data={"count": len(mappings)})
