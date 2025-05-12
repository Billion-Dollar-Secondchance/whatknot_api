# app/api/routes/mystery_moodbox_prompted_question.py

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

@router.get("/today")
def get_today_prompt(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from datetime import timedelta

    today = (datetime.utcnow() + timedelta(hours=5, minutes=30)).date()
    print("📆 IST Adjusted Date:", today)

    pair = db.query(PartnerPairing).filter(
        ((PartnerPairing.user_id == current_user.user_id) |
         (PartnerPairing.partner_id == current_user.user_id)),
        PartnerPairing.pair_status == "active"
    ).first()

    if not pair:
        return failure_response("No active pair found")

    prompt = (
        db.query(MysteryMoodboxPromptedQuestion)
        .join(MysteryMoodboxQuestion, MysteryMoodboxPromptedQuestion.question_id == MysteryMoodboxQuestion.question_id)
        .filter(
            MysteryMoodboxPromptedQuestion.prompted_user_id == current_user.user_id,
            MysteryMoodboxPromptedQuestion.pair_id == pair.pair_id,
            sa.func.date(MysteryMoodboxPromptedQuestion.created_at) == today
        )
        .order_by(MysteryMoodboxPromptedQuestion.created_at.desc())
        .first()
    )

    if not prompt:
        return failure_response("No prompt found for today")

    return success_response("Prompt retrieved successfully", {
        "prompt_id": prompt.prompt_id,
        "pair_id": prompt.pair_id,
        "question_id": prompt.question_id,
        "prompted_user_id": prompt.prompted_user_id,
        "question_text": prompt.question.question_text,
        "options": prompt.question.options,
        "created_at": prompt.created_at,
        "prompt_status": prompt.prompt_status,
    })


@router.post("/submit")
def submit_prompt_response(
    payload: SubmitPromptResponse,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print(f"🧾 Current User: {current_user.user_id}")
    print(f"📩 Payload Prompt ID: {payload.prompt_id}")

    pair = db.query(PartnerPairing).filter(
        ((PartnerPairing.user_id == current_user.user_id) |
         (PartnerPairing.partner_id == current_user.user_id)),
        PartnerPairing.pair_status == "active"
    ).first()

    if not pair:
        print("🚫 No active pair found.")
        return failure_response("No active pair found")

    print(f"✅ Active Pair ID: {pair.pair_id}")

    prompt = db.query(MysteryMoodboxPromptedQuestion).filter(
        MysteryMoodboxPromptedQuestion.prompt_id == payload.prompt_id,
        MysteryMoodboxPromptedQuestion.prompted_user_id == current_user.user_id,
        MysteryMoodboxPromptedQuestion.pair_id == pair.pair_id
    ).first()

    print(f"🔍 Fetched Prompt: {prompt}")

    if not prompt:
        return failure_response("Prompt not found for this user")

    prompt.answer = payload.answer
    prompt.prompt_status = "answered_by_one"
    prompt.updated_at = datetime.utcnow()

    db.commit()
    print("✅ Answer submitted successfully")
    return success_response("Prompt response submitted successfully")


@router.get("/guess-prompt-question")
def get_guess_prompt_question(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pair = db.query(PartnerPairing).filter(
        ((PartnerPairing.user_id == current_user.user_id) |
         (PartnerPairing.partner_id == current_user.user_id)),
        PartnerPairing.pair_status == "active"
    ).first()

    if not pair:
        raise HTTPException(status_code=404, detail="No active pair found")

    prompt = db.query(MysteryMoodboxPromptedQuestion).filter(
        MysteryMoodboxPromptedQuestion.pair_id == pair.pair_id,
        MysteryMoodboxPromptedQuestion.prompted_user_id != current_user.user_id
    ).order_by(MysteryMoodboxPromptedQuestion.created_at.desc()).first()

    if not prompt:
        return failure_response("No prompt found to guess")

    partner = db.query(User).filter(User.user_id == prompt.prompted_user_id).first()

    if partner and partner.name:
        personalized_question = f"Can you guess what made {partner.name} smile today?"
    else:
        personalized_question = "Can you guess what made your partner smile today?"

    return success_response("Prompt retrieved for guessing", {
        "prompt_id": str(prompt.prompt_id),
        "question": personalized_question
    })


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

    if prompt.guess_text is not None:
        return success_response("Guess already submitted", {
            "answer_matched": prompt.answer_matched,
            "streak_count": None,
            "badge": None,
            "reveal_answer": not prompt.answer_matched,
            "correct_answer": prompt.answer if not prompt.answer_matched else None
        })

    prompt.guesser_id = current_user.user_id
    prompt.guess_text = payload.guess_text
    prompt.guessed_at = datetime.utcnow()

    is_match = False
    if prompt.answer and payload.guess_text:
        is_match = prompt.answer.strip().lower() == payload.guess_text.strip().lower()
        prompt.answer_matched = is_match

    if prompt.prompt_status == "answered_by_one":
        prompt.prompt_status = "answered_by_both"

    db.commit()

    result = update_streak_logic(db, prompt.pair_id, is_match)

    return success_response(message="Guess submitted successfully", data={
        "answer_matched": is_match,
        "streak_count": result["streak_count"],
        "badge": result["badge"],
        "reveal_answer": not is_match,
        "correct_answer": prompt.answer if not is_match else None
    })
