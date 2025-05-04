from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import sqlalchemy as sa
from uuid import UUID
from app.db.models.mystery_moodbox_prompted_questions import MysteryMoodboxPromptedQuestion
from app.db.models.mystery_moodbox_questions import MysteryMoodboxQuestion
from app.schemas.mystery_moodbox_prompted_question import MysteryMoodboxPromptedQuestionResponse,SubmitPromptResponse,SubmitGuessRequest
from app.dependencies.auth import get_current_user, get_db
from app.db.models.user import User
from app.utils.response_format import success_response, failure_response
from app.db.models.partner_pairing import PartnerPairing
from app.utils.response_format import success_response, failure_response
from app.services.streak import update_streak_logic

router = APIRouter()

@router.get("/today", response_model=MysteryMoodboxPromptedQuestionResponse)
def get_today_prompt(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = datetime.utcnow().date()

    prompt = (
        db.query(MysteryMoodboxPromptedQuestion)
        .join(MysteryMoodboxQuestion, MysteryMoodboxPromptedQuestion.question_id == MysteryMoodboxQuestion.question_id)
        .filter(
            MysteryMoodboxPromptedQuestion.prompted_user_id == current_user.user_id,
            sa.func.date(MysteryMoodboxPromptedQuestion.created_at) == today
        )
        .order_by(MysteryMoodboxPromptedQuestion.created_at.desc())
        .first()
    )

    print("🔍 Queried user_id:", current_user.user_id)
    print("📆 Date:", today)
    print("🎯 Prompt Found:", prompt)

    if not prompt:
        return {"status": "failure", "message": "No prompt found for today", "data": None}

    # Print contents for debugging
    print("🧠 Question Text:", prompt.question.question_text)
    print("🗂 Options:", prompt.question.options)

    return {
        "status": "success",
        "message": "Prompt retrieved successfully",
        "data": MysteryMoodboxPromptedQuestionResponse(
        
        prompt_id=prompt.prompt_id,
        pair_id=prompt.pair_id,
        question_id=prompt.question_id,
        prompted_user_id=prompt.prompted_user_id,
        question_text=prompt.question.question_text,
        options=prompt.question.options,
        created_at=prompt.created_at,
        prompt_status=prompt.prompt_status,
    )}


# @router.post("/submit")
# def submit_prompt_response(
#     payload: SubmitPromptResponse,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     prompt = db.query(MysteryMoodboxPromptedQuestion).filter(
#         MysteryMoodboxPromptedQuestion.prompt_id == payload.prompt_id,
#         MysteryMoodboxPromptedQuestion.prompted_user_id == current_user.user_id
#     ).first()

#     if not prompt:
#         return failure_response("Prompt not found for this user")

#     prompt.prompt_status = "answered_by_one"
#     prompt.updated_at = datetime.utcnow()

#     db.commit()
#     return success_response("Prompt response submitted successfully")

@router.post("/submit")
def submit_prompt_response(
    payload: SubmitPromptResponse,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prompt = db.query(MysteryMoodboxPromptedQuestion).filter(
        MysteryMoodboxPromptedQuestion.prompt_id == payload.prompt_id,
        MysteryMoodboxPromptedQuestion.prompted_user_id == current_user.user_id
    ).first()

    if not prompt:
        return failure_response("Prompt not found for this user")

    # ✅ Save the answer
    prompt.answer = payload.answer
    prompt.prompt_status = "answered_by_one"
    prompt.updated_at = datetime.utcnow()

    db.commit()
    return success_response("Prompt response submitted successfully")


@router.get("/guess-prompt-question")
def get_guess_prompt_question(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Find the active pair involving the current user
    pair = db.query(PartnerPairing).filter(
        ((PartnerPairing.user_id == current_user.user_id) |
         (PartnerPairing.partner_id == current_user.user_id)),
        PartnerPairing.pair_status == "active"
    ).first()

    if not pair:
        raise HTTPException(status_code=404, detail="No active pair found")

    # 2. Find the latest prompted question for the *other* user (to guess)
    prompt = db.query(MysteryMoodboxPromptedQuestion).filter(
        MysteryMoodboxPromptedQuestion.pair_id == pair.pair_id,
        MysteryMoodboxPromptedQuestion.prompted_user_id != current_user.user_id
    ).order_by(MysteryMoodboxPromptedQuestion.created_at.desc()).first()

    if not prompt:
        return failure_response("No prompt found to guess")

    # 3. Get the original question
    question_text = prompt.question.question_text

    # 4. Replace with natural guess phrasing
    partner = db.query(User).filter(User.user_id == prompt.prompted_user_id).first()

    if partner and partner.name:
        personalized_question = f"Can you guess what made {partner.name} smile today?"
    else:
        personalized_question = "Can you guess what made your partner smile today?"

    return success_response("Prompt retrieved for guessing", {
        "prompt_id": str(prompt.prompt_id),
        "question": personalized_question
    })


# @router.post("/submit-guess")
# def submit_guess(
#     payload: SubmitGuessRequest,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     prompt = db.query(MysteryMoodboxPromptedQuestion).filter(
#         MysteryMoodboxPromptedQuestion.prompt_id == payload.prompt_id
#     ).first()

#     if not prompt:
#         return failure_response("Prompt not found")

#     prompt.guesser_id = current_user.user_id
#     prompt.guess_text = payload.guess_text
#     prompt.guessed_at = datetime.utcnow()

#     if prompt.answer and payload.guess_text:
#         prompt.answer_matched = (
#             prompt.answer.strip().lower() == payload.guess_text.strip().lower()
#         )

#     if prompt.prompt_status == "answered_by_one":
#         prompt.prompt_status = "answered_by_both"

#     db.commit()

#     # Automatically trigger streak update
    
#     update_streak_logic(db, prompt.pair_id, prompt.answer_matched)
#     streak_info = update_streak_logic(db, prompt.pair_id, prompt.answer_matched)
#     if prompt.guess_text is not None:
#         return success_response("Guess already submitted", {
#         "answer_matched": prompt.answer_matched,
#         "streak_count": streak_info.get("streak_count"),
#         "badge_unlocked": streak_info.get("badge")
#     })

# app/api/routes/mystery_moodbox_prompted_question.py

@router.post("/submit-guess")
def submit_guess(
    payload: SubmitGuessRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prompt = db.query(MysteryMoodboxPromptedQuestion).filter(
        MysteryMoodboxPromptedQuestion.prompt_id == payload.prompt_id
    ).first()

    if not prompt:
        return failure_response("Prompt not found")

    # Prevent double submission
    if prompt.guess_text is not None:
        return success_response("Guess already submitted", {
            "answer_matched": prompt.answer_matched,
            "streak_count": None,
            "badge": None
        })

    # Record guess
    prompt.guesser_id = current_user.user_id
    prompt.guess_text = payload.guess_text
    prompt.guessed_at = datetime.utcnow()

    if prompt.answer and payload.guess_text:
        prompt.answer_matched = (
            prompt.answer.strip().lower() == payload.guess_text.strip().lower()
        )

    if prompt.prompt_status == "answered_by_one":
        prompt.prompt_status = "answered_by_both"

    db.commit()

    # Trigger streak + badge logic
    from app.services.streak import update_streak_logic
    result = update_streak_logic(db, prompt.pair_id, prompt.answer_matched)

    return success_response(message="Guess submitted successfully", data={
        "answer_matched": prompt.answer_matched,
        "streak_count": result["streak_count"],
        "badge": result["badge"]
    })
